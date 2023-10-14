from django import forms 
from django.forms import PasswordInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.password_validation import validate_password




"""
widget are adding to allow us style the forms in the templates
read more about the widgets.
"""
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'city')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'userfield'}),
            'email': forms.EmailInput(attrs={'class': 'emailfield'}),
            'password1': forms.PasswordInput(attrs={'class': 'passwordfield'}),
            'password2': forms.PasswordInput(attrs={'class': 'passwordfield'}),
            'city': forms.TextInput(attrs={'class': 'cityfield'}),
        }



class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'loginuser'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'loginpassword'}))
    



class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='New Email', widget=forms.EmailInput)

    def clean_email(self):
        email  = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('This Email is already in use.')
        else:
            return email 
        

class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password





   


# asking user input their password before deleting their account
class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=PasswordInput)