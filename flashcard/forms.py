from django import forms
from .models import FlashcardCategory, Flashcard



class FlashcardcategoryCreationForm(forms.Form):
    class Meta:
        model = FlashcardCategory
        fields = '__all__'


class FlashcardCreationForm(forms.Form):
    class Meta:
        model = Flashcard
        fields = '__all__'


class FlashcardInteractionForm(forms.Form):
    action = forms.ChoiceField(choices=[('flip', 'Flip Card'), ('next', 'Next Card')])
