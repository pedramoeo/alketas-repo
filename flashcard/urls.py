from django.urls import path
from .views import *



urlpatterns = [
    path('flashcard/latest/', LatestView.as_view(), name='latest_flashcard_category'),
    path('api/flashcard/latest/', LatestAPIView.as_view(), name='latest_flashcard_category_api'),
    path('categories/page/<int:page>', AllFlashcardCategoryView.as_view(), name='all_categories'),
    path('categories/<str:category_name>/page/<int:page>', FlashcardCategoryPageView.as_view(), name='each_category_page'),
    path('flashcards/page/<int:page>', FlashcardView.as_view(), name='all_flashcards'),


]