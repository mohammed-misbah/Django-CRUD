from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee

# for form fields 
class EmployeeForm(forms.ModelForm):
    class Meta:
        model =Employee
        #we mentioned model items imported to form fieldsj
        fields =('username','password','mobile','email','Place') 
        #set password as hidden format
        widgets = {
            'password':forms.PasswordInput()
        }
        #name changing using label
        labels = {
            'username':'User Name',
            'email':'E-mail'
        }


        # while select a position list it hold and drag the control as list
    def __init__(self,*args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)

        # set select as transparent
        self.fields['Place'].empty_label ="select" 

       # remove requered validation '*' remove
        self.fields['username'].required=False 
        self.fields['password'].required=False 
        self.fields['mobile'].required=False  
        self.fields['email'].required=False
        # self.fields['place'].required=False    

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
       