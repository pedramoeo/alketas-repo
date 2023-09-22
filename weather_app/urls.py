from django.urls import path
from .views import *

urlpatterns = [
    path('weather/', WeatherView.as_view(), name='weather-app'),
    path('weather/results/<str:city>', WeatherResultsView.as_view(), name='search_results'),
    path('api/weather/', WeatherAPIView.as_view(), name='weather-app_api'),
    path('api/weather/results/<str:city>', WeatherResultsAPIView.as_view(), name='search_results_api'),


]
