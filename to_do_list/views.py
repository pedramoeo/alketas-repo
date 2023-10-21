from typing import Any
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.conf import settings



from account.models import CustomUser
from .models import Category, Task
from .forms import *
from .serializers import *


from django.views.generic import View, ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django_user_agents.utils import get_user_agent
from django.contrib.auth import get_user_model
from django.contrib.messages import constants as messages

from django.utils import timezone
import datetime


from rest_framework.pagination import PageNumberPagination






User = get_user_model()


class CustomPagination(PageNumberPagination):
    def get_page_size(self, request):
        user_agent = get_user_agent(request)
        if user_agent.is_mobile:
            return 6
        else:
            return 10




class LatestView(ListView):
    template_name = 'todo-latest.html'

    def get(self, request, *args, **kwargs):
        
        task_list = Task.objects.all().order_by('-date_created')[:5]
        category_list = Category.objects.all().order_by('-date_created')[:5]

        context = {
            "task_list": task_list,
            "category_list": category_list,
        }
        return render(request, self.template_name, context)
    
    





# 1 - for the main latests' page of the to do list app


class AllCategoryView(ListView):
    template_name = "todo-list/all-todo-categories.html"
    model = Category
    paginator_class = CustomPagination

    def get_queryset(self):
        sort_order_category = self.request.GET.get('sort_order_category', 'date_created')

        if sort_order_category == "newest":
            queryset = Category.objects.filter(user=self.request.user).order_by('-date_created')
        elif sort_order_category == "oldest":
            queryset = Category.objects.filter(user=self.request.user).order_by('date_created') 
        elif sort_order_category == "category_colour":
            queryset = Category.objects.filter(user=self.request.user).order_by('category_colour')
        elif sort_order_category == "is_pinned":
            queryset = Category.objects.filter(user=self.request.user).order_by('-is_pinned')
        else:
            queryset = Category.objects.filter(user=self.request.user)

        
        return queryset
    

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if "add_category" in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()
            else:
                # rerender the form if it wasn't valid
                return self.render_to_response(self.get_context_data(form=form))
            
        elif "delete_category" in request.POST:
            category_id = request.POST.get('category_id')
            try:
                category = Category.objects.get(id=category_id, user=request.user)
                category.delete()
            except Category.DoesNotExist:
                messages.error(request, 'The category does not exist.')
        
        elif "delete_all_categories" in request.POST:
            category_ids = request.POST.getlist('category_ids')
            for category_id in category_ids:
                try:
                    category = Category.objects.filter(id=category_id)
                    category.delete()
                except Category.DoesNotExist:
                    messages.error(request, "The category does not exist.")

        elif "change_category_colour" in request.POST:
            category_id = request.POST.get('category_id')
            new_colour = request.POST.get('new_colour')
            try: 
                category = Category.objects.get(id=category_id)
                category.category_colour = new_colour
                category.save()
            except Category.DoesNotExist:
                messages.error(request, "The category does not exist.")

        elif "mark_category_pinned" in request.POST:
            category_id = request.POST.get('category_id')
            try:
                category = Category.objects.get(id=category_id)
                category.is_pinned = True
                category.save()
            except Category.DoesNotExist:
                messages.error(request, "The category does not exist.")

        elif "mark_category_unpinned" in request.POST:
            category_id = request.POST.get('category_id')
            try:
                category = Category.objects.get(id=category_id)
                category.is_pinned = False
                category.save()
            except Category.DoesNotExist:
                messages.error(request, "The category does not exist.")

    






#viewing list of all categories:



class CategoryPageView(ListView):
    model = Category
    template_name = "todo-list/category-page.html"
    context_object_name = 'tasks'
    paginator_class = CustomPagination

    

    def get_queryset(self):
        category_name = self.kwargs['category']
        sort_order_category = self.kwargs.get('sort_order_category', 'date_created')
        queryset = Task.objects.filter(category__category_name=category_name, user=self.request.user)

        if sort_order_category == "newest":
            queryset = queryset.order_by('-date_created')
        elif sort_order_category == "oldest":
            queryset = queryset.order_by('date_created')
        elif sort_order_category == "is_pinned":
            queryset = queryset.order_by('-is_pinned')
        elif sort_order_category == "is_complete":
            queryset = queryset.order_by('-is_complete')
        elif sort_order_category == "due_time":
            queryset = queryset.order_by('-due_time')

        return queryset
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the Category object
        category_name = self.kwargs['category']
        category = Category.objects.get(category_name=category_name)
        # Add the category to the context
        context['category'] = category
        return context

    

    def post(self, request, *args, **kwargs):
        user = self.request.user
        category = self.kwargs['category']

        if "add_task" in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = user
                task.category = category
                task.save()
                return redirect('category-page')
            else:
                return render(request, self.template_name, {'form': form})

        elif "delete_task" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id, category=category, user=user)
                task.delete()
            except Task.DoesNotExist:
                messages.error(request, "Task does not exist.")
            
        elif "delete_all_tasks" in request.POST:
            task_ids = request.POST.getlist('task_ids')
            for task_id in task_ids:
                try:
                    task = Task.objects.get(id=task_id, category=category, user=user)
                    task.delete()
                except:
                    messages.error(request, "Task cannot be deleted.")

        elif "mark_task_pinned" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id, category=category, user=user)
                task.is_pinned = True
                task.save()
            except:
                messages.error("cannot mark task pinned")
        
        elif "mark_task_unpinned" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id, category=category, user=user)
                task.is_pinend = False
                task.save()
            except:
                messages.error("cannot mark task unpinned")

        elif "mark_task_complete" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id, category=category, user=user)
                task.is_complete = True
                task.save()
            except:
                messages.error("cannot mark task complete")

        elif "mark_task_incomplete" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id, category=category, user=user)
                task.is_complete = False
                task.save()
            except:
                messages.error("cannot mark task incomplete")

        
        elif "change_due_time" in request.POST:
            task_id = request.POST.get('task_id')
            new_due_time = request.POST.get('new_due_time')  # The new due time should be provided in the POST data
            try:
                task = Task.objects.get(id=task_id, category=category, user=user)
                task.due_time = timezone.make_aware(datetime.datetime.strptime(new_due_time, "%Y-%m-%d %H:%M:%S"))
                task.save()
            except Task.DoesNotExist:
                messages.error(request, "Task does not exist.")
            except ValueError:
                messages.error(request, "Invalid date/time format. Please use 'YYYY-MM-DD HH:MM:SS'.")



















# view for displaying all tasks
class TaskView(ListView):
    template_name = 'all-tasks.html'
    model = Task
    paginator_class = CustomPagination


    def get_queryset(self):
        sort_order_task = self.request.GET.get('sort_order_task')
        queryset = Task.objects.filter(user=self.request.user)

        if sort_order_task == "newest":
            queryset = queryset.order_by('-date_created')
        elif sort_order_task == "oldest":
            queryset = queryset.order_by('date_created')
        elif sort_order_task == "is_pinned":
            queryset = queryset.order_by('-is_pinned')
        elif sort_order_task == "is_complete":
            queryset = queryset.order_by('-is_complete')
            
        return queryset
    



    def post(self, request, *args, **kwargs):
        user = self.request.user
         
        if "add_task" in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user= user
                task.save()
                return redirect('todo-tasks')
            else:
                return render(request, self.template_name, {'form': form})
        
        elif "delete_task" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id, user=user)
                task.delete()
            except Task.DoesNotExist:
                messages.error(request, "Task does not exist.")

        elif "delete_all_tasks" in request.POST:
            task_ids = request.POST.getlist('task_ids')
            for task_id in task_ids:
                try:
                    task = Task.objects.get(id=task_id, user=user)
                    task.delete()
                except Task.DoesNotExist:
                    messages.error(request, "Task does not exist.")

        elif "mark_task_pinned" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.is_pinned = True
                task.save()
            except:
                messages.error("Cannot mark task pinned.")

        elif "mark_task_unpinned" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.is_pinned = False
                task.save()
            except:
                messages.error("Cannot mark task unpinned.")

        elif "mark_task_complete" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.is_complete = True
                task.save()
            except:
                messages.error("Cannot mark task complete.")
        
        elif "mark_task_incomplete" in request.POST:
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.is_complete = False
                task.save()
            except:
                messages.error("Cannot mark task incomplete.")

        elif "change_due_time" in request.POST:
            task_id = request.POST.get('task_id')
            new_due_time = request.POST.get('new_due_time')  # The new due time should be provided in the POST data
            try:
                task = Task.objects.get(id=task_id, user=user)
                task.due_time = timezone.make_aware(datetime.datetime.strptime(new_due_time, "%Y-%m-%d %H:%M:%S"))
                task.save()
            except Task.DoesNotExist:
                messages.error(request, "Task does not exist.")
            except ValueError:
                messages.error(request, "Invalid date/time format. Please use 'YYYY-MM-DD HH:MM:SS'.")
















