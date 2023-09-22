from django.urls import path
from .views import *
# in url parameters it's best to initially think about the page number



urlpatterns = [
    path('todo/latest/', LatestView.as_view(), name='lastest_tasks_categories'),
    path('api/todo/latest/', LatestAPIView.as_view(), name='lastest_tasks_categories_api'),
    path('tasks/page/<int:page>', TaskView.as_view(), name='all_tasks'),
    path('categories/page/<int:page>', AllCategoryView.as_view(), name='all_categories'),
    path('api/categories/page/<int:page>', AllCategoryAPIView.as_view(), name='all_categories_api'),
    path('categories/<str:category_name>/page/<int:page>', CategoryPageView.as_view(), name= 'every_category_page'),
    path('api/categories/<int:pk>/page/<int:page>', CategoryPageAPIView.as_view(), name= 'every_category_page_api'),
    
    
]