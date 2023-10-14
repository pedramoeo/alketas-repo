from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from account.models import *
from .models import *
from .forms import *

from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_user_agents.utils import get_user_agent


from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination



User = get_user_model()




class CustomPagination(PageNumberPagination):
    def get_page_size(self, request):
        user_agent = get_user_agent(request)
        if user_agent.is_mobile:
            return 6
        else:
            return 10






# 5 latest flashcards and flashcard categories
class FlashcardLatestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        sort_order_flashcard = request.GET.get('sort_order_flashcard', 'date_created')
        sort_order_category = request.GET.get('sort_order_category', 'date_created')

        if sort_order_flashcard not in ['date_created', '-date_created', 'language', '-language', 'is_pinned', '-is_pinned']:
            sort_order_flashcard = 'date_created'
        
        if sort_order_category not in ['front', '-front', 'is_pinned', '-is_pinned']:
            sort_order_category = 'date_created'


        """
        the queryset method (.none()) is used usually in instances where you need to provide a QuerySet,
        but there isn't one to provide - 
        such as calling a method or to give to a template.
        """

        latest_flashcard = Flashcard.objects.none()
        latest_category = FlashcardCategory.objects.none()

        if request.user.is_authenticated:
            latest_flashcard = Flashcard.objects.filter(user=request.user).order_by(sort_order_flashcard)[:5]
            latest_category = FlashcardCategory.objects.filter(user=request.user).order_by(sort_order_category)[:5]

        category_serializer = FlashcardCategorySerializer(latest_category, many=True)
        flashcard_serializer = FlashcardSerializer(latest_flashcard, many=True)

        context = {
            "latest_flashcardcategory": category_serializer.data,
            "latest_flashcard": flashcard_serializer.data,
            "sort_order_category": sort_order_category,
            "sort_order_flashcard": sort_order_flashcard,
        }

        return Response(context)



class FlashcardLatestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        sort_order_flashcard = request.GET.get('sort_order_flashcard', 'date_created')
        sort_order_category = request.GET.get('sort_order_category', 'date_created')

        if sort_order_flashcard not in ['date_created', '-date_created', 'language', '-language', 'is_pinned', '-is_pinned']:
            sort_order_flashcard = 'date_created'
        
        if sort_order_category not in ['front', '-front', 'is_pinned', '-is_pinned']:
            sort_order_category = 'date_created'


        """
        the queryset method (.none()) is used usually in instances where you need to provide a QuerySet,
        but there isn't one to provide - 
        such as calling a method or to give to a template.
        """

        latest_flashcard = Flashcard.objects.none()
        latest_category = FlashcardCategory.objects.none()

        if request.user.is_authenticated:
            latest_flashcard = Flashcard.objects.filter(user=request.user).order_by(sort_order_flashcard)[:5]
            latest_category = FlashcardCategory.objects.filter(user=request.user).order_by(sort_order_category)[:5]

        category_serializer = FlashcardCategorySerializer(latest_category, many=True)
        flashcard_serializer = FlashcardSerializer(latest_flashcard, many=True)
        

        context = {
            "latest_flashcardcategory": category_serializer.data,
            "latest_flashcard": flashcard_serializer.data,
            "sort_order_category": sort_order_category,
            "sort_order_flashcard": sort_order_flashcard,
        }

        return Response(context)






# viewset for all flashcard categories
class AllFlashcardCategoryAPIVIew(APIView):
    def get(self, request, *args, **kwargs):
        paginator = CustomPagination()

        if request.user.is_authenticated:
            category_id = self.kwargs.get('flashcardcategory_id', None)
            if category_id is not None:
                queryset = FlashcardCategory.objects.filter(user=request.user, id=category_id)
            else:
                queryset = FlashcardCategory.objects.filter(user=request.user)

            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = FlashcardCategorySerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = FlashcardCategorySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)
    
    def post(self, request, *args, **kwargs):
        user = self.request.user

        if "add_category" in request.POST:
            form = FlashcardcategoryCreationForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()

        elif "change_category_language" in request.POST:
            category_id = request.POST.get('flashcardcategory_id')
            new_language = request.POST.get('new_language')
            category = FlashcardCategory.objects.get(id=category_id, user=request.user)
            category.language = new_language
            category.save()

        elif "delete_category" in request.POST:
            category_id = request.POST.get('flashcardcategory_id')
            category = FlashcardCategory.objects.get(id=category_id, user=request.user)
            category.delete()

        elif "delete_all_categories" in request.POST:
            category_ids = request.POST.getlist('flashcardcategory_ids')
            for category_id in category_ids:
                category = FlashcardCategory.objects.get(id=category_id, user=request.user)
                category.delete()

        elif "mark_category_pinned" in request.POST:
            category_id = request.POST.get('flashcardcategory_id')
            category = FlashcardCategory.objects.get(id=category_id, user=request.user)
            category.is_pinned = True
            category.save()

        elif "mark_category_unpinned" in request.POST:
            category_id = request.POST.get('flashcardcategory_id')
            category = FlashcardCategory.objects.get(id=category_id, user=request.user)
            category.is_pinned = False
            category.save()        

        return Response({"message": "Operation completed"})








# each page of every category
class FlashcardCategoryPageAPIView(LoginRequiredMixin, ListView):
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
        flashcards = Flashcard.objects.filter(category_id=category_id)


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







# viewset for all flashcards
class FlashcardAPIView(APIView):
    def get(self, request, *args, **kwargs):
        paginator = CustomPagination()


        if request.user.is_authenticated:
            flashcard_id = self.kwargs.get('flashcard_id', None)

            sort_by = request.query_params.get('sort_by', None)

            if flashcard_id is not None:
                if sort_by == "newest":
                    queryset = Flashcard.objects.filter(id=flashcard_id).order_by('-date_created')
                elif sort_by == "oldest":
                    queryset = Flashcard.objects.filter(id=flashcard_id).order_by('date_created')
                elif sort_by == "is_pinned":
                    queryset = Flashcard.objects.filter(id=flashcard_id).order_by('-is_pinned')

            else:
                queryset = Flashcard.objects.none()

            page = paginator.paginate_queryset(queryset, request)
        
            if page is not None:
                serializer = FlashcardSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
        else:
            return Response({"details": "Authentication credentials were not provided."}, status=401)



