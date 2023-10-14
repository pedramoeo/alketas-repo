from django import forms
from .models import Category, Task 


class CategoryForm(forms.Form):
    class Meta:
        model = Category
        fields = "__all__"


class TaskForm(forms.Form):
    class Meta:
        model = Task
        fields = "__all__"


