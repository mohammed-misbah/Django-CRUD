
from django.urls import path,include
from . import views


urlpatterns = [

    path('', views.employee_form,name='employee_insert'),           #get and post reqst for insert operation     
    path('<int:id>/', views.employee_form,name='employee_update'),   #get and post reqst for update operation 
    path('delete/<int:id>/',views.employee_delete,name='employee_delete'), #delete an employee records from a form
    path('list/',views.employee_list,name='employee_list'),            #get reqst to retrive and display all  records    
    path('signup',views.signup,name='signup'),
    path('login/',views.loginPage,name='login'),
    path('homepage',views.homepage,name='homepage'),
    path('logout/',views.logoutuser,name='logout')
    
    # path('searching/',views.searching,name='searching'),
    # path('signuppage',views.savedata,name='Signup'),
    
]
   