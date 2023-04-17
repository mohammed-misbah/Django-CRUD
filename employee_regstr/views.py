from multiprocessing import context
from django.shortcuts import render,redirect
from django.db.models import Q
from .forms import EmployeeForm
from .models import Employee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.

#-------SIGN-UP PAGE-------#

def signup(request):
    if request.method =='POST':
        username=request.POST['name']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if Employee.objects.filter(username=username).exists():
                messages.info(request,'Username is Taken')
                return redirect('signup')
            elif Employee.objects.filter(email=email).exists():
                messages.info(request,'Email is requered')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email)
                data =Employee()
                data.username=username
                data.email=email
                data.password=password1
                data.save()
                login(request,user)
                print('User Created')
                return redirect('homepage')
        else:
            messages.info(request,'password is not matching')
            return redirect('signup')
        
    else:
        return render(request,'employee_regstr/signup.html')


#--------LOGIN-PAGE------------#

def loginPage(request):
    print(request.method)
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        
        if user:
            login(request,user)
            return redirect('homepage')
        else:
            messages.info(request,'username OR password is incorrect')
            return redirect('login')
    else:
        return render(request,'employee_regstr/login.html')



#---------LOGOUT-PAGE----------#

@login_required(login_url='signup')
def homepage(request):
    return render(request,'employee_regstr/homepage.html')





#--------EMPLOYEE-LIST--------#

def employee_list(request):
    if 'key' in request.GET:
        key = request.GET['key']
        displaylist =Employee.objects.filter(Q(username__icontains=key)|Q(mobile__icontains=key)|Q(email__icontains=key))
    else:
    #display all the values in a employee_list 
        displaylist=Employee.objects.all()
    context = {'employee_list':displaylist}
    return render(request,"employee_regstr/employee_list.html",context)



#--------EMPLOYEE-FORM--------#
def employee_form(request,id=0): #if id not zero then reqst will be updated oprtion else insert oprtion
    if request.method =="GET":    
        if id==0:                                       #get requests
             form = EmployeeForm()
        else:
            employee = Employee.objects.get(pk=id)
            form=EmployeeForm(instance=employee)
        return render(request,"employee_regstr/employee_form.html",{'form':form})
    
     #post requests save the data's that send from the form
    else:
        if id==0:
            form = EmployeeForm(request.POST)   
        else:
             employee = Employee.objects.get(pk=id)
             form = EmployeeForm(request.POST,instance=employee)
             #save a user entered data's
        if form.is_valid():     
            form.save()
            username=form.cleaned_data.get('username') 
            password1=form.cleaned_data.get('password') 
            email=form.cleaned_data.get('email') 
            u=User.objects.create_user(username=username,password=password1,email=email)
            print(username,password1,email)


             #redirect to list of employee datas
        return redirect('/')
# ----------delete form---------------#

def employee_delete(request,id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return redirect('employee_list')
    
    
def logoutuser(request):
    logout(request)
    return redirect('signup')