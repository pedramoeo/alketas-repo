from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),

    path('logout/', logout, name='logout'),


    path('login/', LoginView.as_view(), name='login'),


    path('dashboard/', ProfileView.as_view(), name='dashboard'), 

]