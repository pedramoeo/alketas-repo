from django.urls import path
from .views import *



urlpatterns = [
    path('flashcard/latest/', FlashcardLatestAPIView.as_view(), name='latest_flashcard_category'),


    path('categories/<str:category_name>/page/<int:page>', FlashcardCategoryPageAPIView.as_view(), name='each_category_page'),

    path('flashcards/page/', FlashcardAPIView.as_view(), name='all_flashcards'),


]