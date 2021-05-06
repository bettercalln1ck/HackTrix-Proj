from django import forms
from .models import FileUpload
from .models import UserProfile
from django.contrib.auth.models import User

class file_upload_form(forms.ModelForm):
	class Meta:
		model=FileUpload
		fields=('file',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('space',)
class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Type your username'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Type your password'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'Type your email'}))
    class Meta:
        model=User
        fields=('username','password','email',)

