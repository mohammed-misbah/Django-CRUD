from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import JsonResponse
from accounts.models import Address,Account
from cart.models import CartItem,OldCart,GCart
from orders.models import Orders
from category.models import Products
import uuid
from django.contrib import messages
from coupen.models import Coupens
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from wallet.models import Wallet


@login_required(login_url='adminlogin')
def admin_order_detailes(request):
    orders = Orders.objects.all().order_by('-orderd_date')
    return render(request,"admin/orders.html", {"orders": orders})

def add_address(request):
    if not request.user.is_authenticated:
            messages.info(request ,'Guest')
            return redirect(request.META.get('HTTP_REFERER'))
    user = request.user
    destination = request.META.get('HTTP_REFERER')
    if request.POST:
        first_name = request.POST.get('first_name')
        
        if request.POST['last_name']:
            last_name = request.POST.get('last_name')
    
        phone1 = request.POST.get('phone1')
        if request.POST['phone2']:
            phone2 = request.POST.get('phone2')
        
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        if request.POST['address2']:
            address2 = request.POST.get('address2')

        country = request.POST.get('country')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        payment = request.POST.get('paymentMethod')
        
        if first_name and last_name and address2:
            address = Address.objects.create(user= user, first_name=first_name,
                                             last_name=last_name ,phone_number_1=phone1, 
                                             phone_number_2= phone2, address_1 = address1, 
                                             address_2 = address2, country=country,State=state ,
                                             zip_code = zip_code , email=email
                                             )
            address.save()
            next1 = PreviousUrl.next1
            return redirect(next1)
        else:
            messages.error(request,"please fill the required fields")
    PreviousUrl(destination)
    return render(request, "add_address.html")
class PreviousUrl:
     next1 = None
     def __init__(self,next1) -> None:
        PreviousUrl.next1 = next1
    
def order_place(request,total=0,quantity=0,
                cart_items=None,tax=0,delv=0,
                g_total=0):
    user = request.user
    try : 
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
            for i in cart_items :
                product = Products.objects.get(id = i.product.id)
                get_minus_prod = i.Quantity  
                minus =i.product.quantity-get_minus_prod  
                product.quantity = minus
                product.save()   
        num = 0
        for cart_item in cart_items:
            num = num+1
            if cart_item.product.offer_price is not None:
                total += (cart_item.product.offer_price * cart_item.Quantity)
            else:
                total += (cart_item.product.selling_price * cart_item.Quantity)     
            quantity += cart_item.Quantity
            
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv
            
        new_total=0
        coupen = None
        coupen_didected = 0
        if 'new_price' in request.session:
            
            new_price = request.session['new_price']
            coupen = request.session['coupen']
            if Coupens.objects.filter(coupen_code = coupen).exists():
                coup = Coupens.objects.get(coupen_code = coupen)

            if new_price is not None:
                new_total = new_price
                coupen_price = g_total-new_total
                coupen_didected = coupen_price/num
               
    except :
        if not request.user.is_authenticated:
            messages.info(request ,'You have to login to continue Checkout')
            return redirect(request.META.get('HTTP_REFERER'))
            
    payment = request.POST.get('payment')
    paypal = request.POST.get('paypal')
    if request.POST and payment =='cod':
        
        adrs_id = request.POST.get('add_id')
        to = Address.objects.get(id=adrs_id)
        address_to=to.address_1
        order_id =uuid.uuid4()
        if payment and adrs_id is not None:
            for item in cart_items:
                Orders(product = item.product ,user = request.user , 
                       address= address_to ,total_price = item.sub_total_c(coupen_didected),
                       payment=payment, status = "placed" ,
                       price = item.product.selling_price , 
                       quantity = item.Quantity,order_id = order_id,grand_price = g_total,offered_price = new_total,coupen_applied = coupen,variation_id =item.varient_id).save()
                OldCart(product = item.product,user = request.user , Quantity = item.Quantity).save()
            status = True
            if coupen_didected is not 0:
                coup.is_active = False
                coup.save()
                request.session.pop('coupen',None)
                request.session.pop('new_price',None)
                request.session.modified = True
                return render(request , "order_success.html" ,{"user":user,"g_total":new_total})
            else:
                return JsonResponse({'status': status})

            
    if request.POST and payment =='razorpay':
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')
        adrs_id = request.POST.get('add_id')
        to = Address.objects.get(id=adrs_id)
        address_to=to.address_1
    
        if payment is not None:
            for item in cart_items:
                Orders(product = item.product ,user = request.user , 
                       address= address_to ,total_price = item.sub_total(),
                       payment=payment, status = "placed" ,
                       price = item.product.selling_price , 
                       quantity = item.Quantity, order_id=order_id, payment_id=payment_id,variation_id =item.varient_id).save()
                OldCart(product = item.product,user = request.user , Quantity = item.Quantity).save()
                status = True
            return JsonResponse({'status': status})
        
    if request.POST and paypal =='Paypal':
        order_id = uuid.uuid4()
        payment_id = request.POST.get('payment_id')
        adrs_id = request.POST.get('add_id')
        to = Address.objects.get(id=adrs_id)
        address_to=to.address_1
        if paypal is not None:
            for item in cart_items:
                Orders(product = item.product ,user = request.user , 
                       address= address_to ,total_price = item.sub_total(),
                       payment=paypal, status = "placed" ,
                       price = item.product.selling_price , 
                       quantity = item.Quantity, order_id=order_id, payment_id=payment_id ,variation_id =item.varient_id).save()
                OldCart(product = item.product,user = request.user , Quantity = item.Quantity).save()
                status = True
            return JsonResponse({'status': status})
            
    return redirect("checkout")

@never_cache
def order_success(request,total=0,quantity=0,
                cart_items=None,tax=0,delv=0,
                g_total=0):
    user = request.user
    cart_items = CartItem.objects.filter(user=request.user,is_active=True)
    for cart_item in cart_items:
            if cart_item.product.offer_price is not None:
                total += (cart_item.product.offer_price * cart_item.Quantity)
            else:
                total += (cart_item.product.selling_price * cart_item.Quantity)
            quantity += cart_item.Quantity
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv
    if g_total is 0:
        return redirect('order_status')
    CartItem.objects.filter(user=request.user,is_active=True).delete()
    return render(request , "order_success.html" ,{"user":user,"g_total":g_total})
@never_cache
def order_status(request):
    try:
        orders = Orders.objects.filter(user = request.user).order_by('-orderd_date')
    except:
        return render(request, "order_status.html" )
    return render(request, "order_status.html" ,{"orders":orders})

@never_cache
def order_details(request, id):
    order = Orders.objects.get(id=id)
    id = order.address
    # address = Address.objects.get(id=id)
    return render(request, "order_details.html",{"order":order})

@login_required(login_url='adminlogin')
def admin_orderedit(request):
    order_id = request.GET.get('oid')
    value = request.GET.get('value')
    obj = Orders.objects.get(id = order_id)
    if value == "Refund Initiated":
        price = obj.product.selling_price
        email = request.user
        user = Account.objects.get(email = email)
        wallet=Wallet.objects.get(user = user)
        wallet.amount+=price
        wallet.save()
        
    obj.status = value
    obj.save()
    orders = Orders.objects.all().order_by('id')
    return render(request,"admin/orders_load.html",{"orders":orders})

def ordercancell(request, id):
    order = Orders.objects.get(id=id)
    product = Products.objects.get(id = order.product.id)
    order.status = "cancelled"
    product.quantity += order.quantity
    product.save()
    order.save()
    return redirect('order_status')

@login_required(login_url='adminlogin')
def admin_order_cancell(request):
    id = request.GET.get('id')
    orders = Orders.objects.get(id=id)
    product = Products.objects.get(id = orders.product.id)
    product.quantity += orders.quantity
    product.save()
    orders.status = "cancelled"
    orders.save()
    orders = Orders.objects.all().order_by('id')
    return render(request,"admin/orders_load.html",{"orders":orders})

@never_cache
def return_order(request,id):
    order = Orders.objects.get(id=id)
    order.status="Return Requested waiting for approval"
    order.save()
    return redirect('order_status')

@login_required(login_url='adminlogin')
def approve_return(request):
    id = request.GET.get('id')
    orders = Orders.objects.get(id=id)
    product = Products.objects.get(id = orders.product.id)
    product.quantity += orders.quantity
    product.save()
    orders.status="Return Aproved"
    orders.save()
    orders = Orders.objects.all().order_by('id')
    return JsonResponse({"id":id})

def guest_checkout(request):
    id=request.session.session_key
    if GCart.objects.filter(Guest_id = id).exists():
        
        destination = request.META.get('HTTP_REFERER')
        response = redirect('user_login')
        response.set_cookie('Guest_checkout', {"destination":destination,"Guest_id":id})
        return response

    
def order_invoice(request,id):
    orders = Orders.objects.filter(order_id = id)
    id_= id
    return render(request, "order_invoice.html",{"orders":orders,"id_":id_}) 