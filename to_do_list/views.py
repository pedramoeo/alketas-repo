from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404


from account.models import CustomUser
from .models import Category, Task
from .forms import CategoryForm, TaskForm
from .serializers import *

from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_user_agents.utils import get_user_agent

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated





# Create your views here.

# 1 - for the main latests' page of the to do list app
class LatestView(LoginRequiredMixin, View):
    
    # displaying data only related to the user
    def get(self, request, *args, **kwargs):

        sort_order_task = request.GET.get('sort_order_task', 'date_created')
        sort_order_category = request.GET.get('sort_order_category', 'date_created')

        if sort_order_task not in ['date_created', '-date_created', 'is_complete', '-is_complete', 'is_pinned', '-is_pinned', 'due_time', '-due_time']:
            sort_order_task = 'date_created'

        if sort_order_category not in ['date_created', '-date_created', 'is_pinned', '-is_pinned', 'category_colour', '-category_colour']:
            sort_order_category = 'date_created'

        latest_category = Category.objects.filter(user=request.user).order_by(sort_order_category)[:5]
        latest_task = Task.objects.filter(user=request.user).order_by(sort_order_task)[:5]

        context = {
            'latest_category': latest_category,
            'latest_task': latest_task,
            'sort_order_task': sort_order_task,
            'sort_order_category': sort_order_category,
        }

        return render(request, 'lastest.html', context)




class LatestAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            user = None

        sort_order_task = request.GET.get('sort_order_task', 'date_created')
        sort_order_category = request.GET.get('sort_order_category', 'date_created')

        if sort_order_task not in ['date_created', '-date_created', 'is_complete', '-is_complete', 'is_pinned', '-is_pinned', 'due_time', '-due_time']:
            sort_order_task = 'date_created'

        if sort_order_category not in ['date_created', '-date_created', 'is_pinned', '-is_pinned', 'category_colour', '-category_colour']:
            sort_order_category = 'date_created'

        latest_category = Category.objects.filter(user=user).order_by(sort_order_category)[:5]
        latest_task = Task.objects.filter(user=user).order_by(sort_order_task)[:5]

        category_serializer = CategorySerializer(latest_category, many=True)
        task_serializer = TaskSerializer(latest_task, many=True)

        return Response({
            'latest_category': category_serializer.data,
            'latest_task': task_serializer.data,
            'sort_order_task': sort_order_task,
            'sort_order_category': sort_order_category,
        })
        




# for the webpage dedicated to viewing list of all categories
class AllCategoryView(LoginRequiredMixin, ListView):
    template_name = 'categories.html'
    model = Category
    
    def get_paginate_by(self, queryset):
        user_agent = get_user_agent(self.request)
        if user_agent.is_mobile:
            return 5
        else:
            return 8

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        if category_id is not None:
            queryset = Category.objects.filter(user=self.request.user, id=category_id)
        else:
            queryset = Category.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if "add_category" in request.POST:
            form = FlashcardcategoryCreationForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()

        elif "change_category_colour" in request.POST:
            category_id = request.POST.get('category_id')
            new_colour = request.POST.get('new_colour')
            category = Category.objects.get(id=category_id, user=request.user)
            category.category_colour = new_colour
            category.save()

        elif "delete_category" in request.POST:
            category_id = request.POST.get('category_id')
            category = Category.objects.get(id=category_id, user=request.user)
            category.delete()
            return redirect('categories')
        
        elif "delete_all_categories" in request.POST:
            category_ids = request.POST.getlist('category_ids')
            for category_id in category_ids:
                category = Category.objects.get(id=category_id, user=request.user)
                category.delete()
            return redirect('categories')
        



class AllCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        category_id = self.kwargs.get('category_id', None)
        if category_id is not None:
            queryset = Category.objects.filter(user=request.user, id=category_id)
        else:
            queryset = Category.objects.filter(user=request.user)
        # Serialize the data
        category_serializer = CategorySerializer(queryset, many=True)
        return Response(category_serializer.data)


    def post(self, request, *args, **kwargs):
        user = request.user

        if "add_category" in request.data:
            form = FlashcardcategoryCreationForm(request.data)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return Response({"message": "Category added successfully"}, status=status.HTTP_201_CREATED)

        elif "change_category_colour" in request.data:
            category_id = request.data.get('category_id')
            new_colour = request.data.get('new_colour')
            category = Category.objects.get(id=category_id, user=request.user)
            category.category_colour = new_colour
            category.save()
            return Response({"message": "Category colour changed successfully"}, status=status.HTTP_200_OK)

        elif "delete_category" in request.data:
            category_id = request.data.get('category_id')
            category = Category.objects.get(id=category_id, user=request.user)
            category.delete()
            return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)

        elif "delete_all_categories" in request.data:
            category_ids = request.data.getlist('category_ids')
            for category_id in category_ids:
                category = Category.objects.get(id=category_id, user=request.user)
                category.delete()
            return Response({"message": "All categories deleted successfully"}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)











# for the webpage after opening a category
class CategoryPageView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'task-category.html'

    def get_paginate_by(self, queryset):
        user_agent = get_user_agent(self.request)
        if user_agent.is_mobile:
            return 5
        else:
            return 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(category=self.get_object())
        context['form'] = TaskForm()  # Add the form to the context
        return context

    def get_object(self):
        return get_object_or_404(Category, id=self.kwargs.get('pk'))

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.category = self.get_object()
            task.save()
            return redirect('category_page', pk=task.category.id)



class CategoryPageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, page=None, format=None):
        category = self.get_object(pk)
        tasks = Task.objects.filter(category=category)
        # Implement pagination logic here based on the 'page' argument
        task_serializer = TaskSerializer(tasks, many=True)
        return Response(task_serializer.data)


    def post(self, request, pk, format=None):
        category = self.get_object(pk)
        form = TaskForm(request.data)
        if form.is_valid():
            task = form.save(commit=False)
            task.category = category
            task.save()
            return Response({"message": "Task added successfully"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)











# displaying all tasks
class TaskView(LoginRequiredMixin, ListView):
    template_name = 'tasks.html'
    model = Task

    def get_paginate_by(self, queryset):
        user_agent = get_user_agent(self.request)
        if user_agent.is_mobile:
            return 5
        else:
            return 8

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        task_id = self.kwargs.get('task_id', None)
        if task_id is not None:
            queryset = Task.objects.filter(category_id=category_id, id=task_id, user=self.request.user)
        else:
            queryset = Task.objects.filter(user=self.request.user)
        return queryset


    def post(self, request, *args, **kwargs):
        user = self.request.user
        if "add_task" in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()

        elif "delete_task" in request.POST:
            task_id = request.POST.get('task_id')

            """ 
            below is a method provided by the manager to retrieve a single object that matches 
            the given lookup parameters. In this case, it’s looking for a Task that has an id equal to task_id and a user equal to request.user.
            """
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()
            return redirect('tasks')
        
        elif "delete_all_tasks" in request.POST:
            task_ids = request.POST.getlist('task_ids')
            for task_id in task_ids:
                task = Task.objects.get(id=task_id, user=request.user)
                task.delete()
            return redirect('tasks')
        
        elif "change_task_category" in request.POST:
            task_id = request.POST.get('task_id')
            new_category_id = request.POST.get('new_category')
            new_category = Category.objects.get(id=new_category_id, user=request.user)
            task = Task.objects.get(id=task_id, user=request.user)
            task.category = new_category
            task.save()

        elif "mark_task_complete" in request.POST:
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id, user=request.user)
            task.is_complete = True
            task.save()

        elif "mark_task_incomplete" in request.POST:
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id, user=request.user)
            task.is_complete = False
            task.save()

        elif "mark_task_pinned" in request.POST:
            task = request.POST.get('task_id')
            task = Task.objects.get(id=task_id, user=request.user)
            task.is_pinned = True
            task.save()

        elif "mark_task_unpinned" in request.POST:
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id, user=request.user)
            task.is_pinned = False
            task.save()

        elif "change_due_time" in request.POST:
            from datetime import datetime

            task_id = request.POST.get('task_id')
            new_due_time_str = request.POST.get('new_due_time')
            new_due_time = datetime.strptime(new_due_time_str, "%Y-%m-%d %H:%M:%S")
            task = Task.objects.get(id=task_id, user=request.user)
            task.due_time = new_due_time
            task.save()
            

        
        









