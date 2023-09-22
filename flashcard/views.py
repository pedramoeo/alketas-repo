from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from account.models import *
from .models import *
from .forms import *
from .serializers import *

from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_user_agents.utils import get_user_agent

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated




# Create your views here.
class LatestView(LoginRequiredMixin, View):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

    

        sort_order_flashcard = request.GET.get('sort_order_task', 'date_created')
        sort_order_flashcard_category = request.GET.get('sort_order_category', 'date_created')

        if sort_order_flashcard not in ['date_created', '-date_created', 'is_pinned', '-is_pinned', 'due_time', '-due_time']:
            sort_order_flashcard = 'date_created'

        if sort_order_flashcard_category not in ['date_created', '-date_created', 'is_pinned', '-is_pinned', 'language', '-language']:
            sort_order_flashcard_category = 'date_created'


        latest_cards = Flashcard.objects.filter(user=request.user).order_by('-front')[:5]
        latest_categories = FlashcardCategory.objects.filter(user=request.user).order_by('-category_name')[:5]


        context = {
            'latest_cards': latest_cards,
            'latest_categories': latest_categories,
        }
        return render(request, 'flashcard.html', context)
    


class LatestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # making sure that the authenticated user is having access
        try:
            user = CustomUser.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            user = None


        sort_order_flashcard = request.GET.get('sort_order_task', 'date_created')
        sort_order_flashcard_category = request.GET.get('sort_order_category', 'date_created')

        if sort_order_flashcard not in ['date_created', '-date_created', 'is_pinned', '-is_pinned', 'due_time', '-due_time']:
            sort_order_flashcard = 'date_created'

        if sort_order_flashcard_category not in ['date_created', '-date_created', 'is_pinned', '-is_pinned', 'language', '-language']:
            sort_order_flashcard_category = 'date_created'

        latest_cards = Flashcard.objects.filter(user=user).order_by('-front')[:5]
        latest_categories = FlashcardCategory.objects.filter(user=user).order_by('-category_name')[:5]

        card_serializer = FlashcardSerializer(latest_cards, many=True)
        category_serializer = FlashcardCategorySerializer(latest_categories, many=True)



        return Response({
            'latest_cards': card_serializer.data,
            'latest_categories': category_serializer.data,
        })












class AllFlashcardCategoryView(LoginRequiredMixin, ListView):
    model = FlashcardCategory
    template_name = 'all-category.html'

    def get_paginate_by(self, queryset):
        user_agent = get_user_agent(self.request)
        if user_agent.is_mobile:
            return 5
        else:
            return 8


    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        if category_id is not None:
            queryset = FlashcardCategory.objects.filter(user=self.request.user, id=category_id)
        else:
            queryset = FlashcardCategory.objects.filter(user=self.request.user)
        return queryset
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if "add_category" in request.POST:
            form = FlashcardcategoryCreationForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()

        elif "delete_category" in request.POST:
            Flashcardcategory_id = request.POST.get('flashcardcategory_id', None)
            categories = FlashcardCategory.objects.filter(user=self.request.user, id=Flashcardcategory_id)
            categories.delete()

        elif "delete_all_categories" in request.POST:
            flashcardcategory_ids = request.POST.getlist('flashcardcategory_ids', None)
            for flashcardcategory_id in flashcardcategory_ids:
                categories = FlashcardCategory.objects.filter(user=self.request.user, id=flashcardcategory_id)
                categories.delete()

        elif "change_category_language" in request.POST:
            flashcardcategory_id = request.POST.get('flashcardcategory_id', None)
            new_language = request.POST.get('new_language')
            category = FlashcardCategory.objects.get(user=self.request.user, id=flashcardcategory_id)
            category.language = new_language
            category.save()

















# each page of every category
class FlashcardCategoryPageView(LoginRequiredMixin, ListView):
    model = FlashcardCategory
    template_name = 'flashcard-category.html'

    def get_paginate_by(self, queryset):
        user_agent = get_user_agent(self.request)
        if user_agent.is_mobile:
            return 6
        else:
            return 9


    """
    here get context data is used to to fetch data from flashcard mode since
    ListView here mainly uses FlashcardCategory models
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category_name = self.kwargs.get('category_name')
        flashcards = Flashcard.objects.filter(category__id=category_id)


        sort_by = self.request.GET.get('sort_by', None)
        if sort_by is not None:
            if sort_by == 'newest':
                flashcards = flashcards.order_by('-date_created')
            elif sort_by == 'oldest':
                flashcards = flashcards.order_by('date_created')
            elif sort_by == 'is_pinned':
                flashcards = flashcards.order_by('-is_pinned')

        context['flashcards'] = flashcards
        return context



    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category_name = self.kwargs.get('category_name')
        return FlashcardCategory.objects.filter(user=self.request.user, id=category_id)







class FlashcardView(ListView):
    model = Flashcard
    template_name = 'flashcards.html'  # replace with your template name

    def get_paginate_by(self, queryset):
        user_agent = get_user_agent(self.request)
        if user_agent.is_mobile:
            return 6
        else:
            return 9

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        sort_by = self.request.GET.get('sort_by', None)
        if sort_by is not None:
            if sort_by == 'newest':
                queryset = queryset.order_by('-date_created')
            elif sort_by == 'oldest':
                queryset = queryset.order_by('date_created')
            elif sort_by == 'is_pinned':
                queryset = queryset.order_by('-is_pinned')

        return queryset





