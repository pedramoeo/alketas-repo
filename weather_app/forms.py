from django import forms
from account.models import CustomUser



class CityForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'cityfield'}))

    class Meta:
        model = CustomUser
        fields = ('city',)