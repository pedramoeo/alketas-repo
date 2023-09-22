from django import forms 
from django.forms import PasswordInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile
from django.contrib.auth import get_user_model, password_validation





class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email', 'password1', 'password2', 'city')




class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))




class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='New Email', widget=forms.EmailInput)

    def clean_email(self):
        email  = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('This Email is already in use.')
        else:
            return email 
        

class ProfilePictureForm(forms.Form):
    class Meta:
        model = Profile 
        fields = ['profile_picture']

    def clean_profile_picture(self):
        Profile_picture = self.cleaned_data.get('Profile_picture', False)
        if Profile_picture:
            if Profile_picture.size > 10*1024*1024:
                raise forms.ValidationError("Image file too large ( > 10mb )")
            return Profile_picture
        else:
            raise forms.ValidationError("Couldn't read uploaded image")
        


# asking user input their password before deleting their account
class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=PasswordInput)