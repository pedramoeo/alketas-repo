from django import forms
from .models import Category, Task 


class CategoryForm(forms.Form):
    class Meta:
        model = Category
        fields = ('category_name', 'category_colour', 'is_pinned',)


class TaskForm(forms.Form):
    class Meta:
        model = Task
        fields = ('category', 'title', 'description', 'is_complete', 'is_pinned', 'due_time')


