from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_view, name='signup-page'),
    path('api/signup/', signup_view_api, name='signup-page_api'),
    path('logout/', logout_view, name='logout'),
    path('api/logout/', logout_api_view, name='logout_api'),
    path('login/', login_view, name='loginview-page'),
    path('api/login/', login_api_view, name='loginview_page_api'),
    path('dashboard/<str:username>/', ProfileView.as_view(), name='profile_dashboard'), 
    path('api/dashboard/<str:username>/', ProfileAPIView.as_view(), name='profile_dashboard_api'), 

]