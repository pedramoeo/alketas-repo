from django.urls import path
from .views import *
# in url parameters it's best to initially think about the page number



urlpatterns = [
    path('todo-latest/', LatestView.as_view(), name='todo-latest'),
    
    path('tasks/page/<int:page>', TaskView.as_view(), name='all_tasks'),

    #path('categories/page/', AllCategoryAPIView.as_view(), name='all_categories'),
    path('categories/page/<int:page>', AllCategoryView.as_view(), name='all-todo-categories'),

    path('todo/<str:category>/', CategoryPageView.as_view(), name= 'category-page'),
    
    
]