from django import forms
from .models import User, cars

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']

class loginform(forms.Form):  
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  

class CarForm(forms.ModelForm):
    class Meta:
        model = cars
        exclude = ['owner', 'is_approved', 'image']

class updateprofileform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
       
        fields = ['first_name', 'last_name',  'phone_number','profile_picture']