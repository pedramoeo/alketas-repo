from django import forms
from account.models import CustomUser



class CityForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('city',)
