from django.views import View
from django.shortcuts import render, redirect 
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from .models import *
from .forms import CityForm
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WeatherInfoSerializer



class WeatherView(LoginRequiredMixin, View):

    # we write a unique specific function to fetch data from Open Weather for the sake of code reusability 
    def get_weather(self, city):
        api_key = settings.OPENWEATHER_API_KEY
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q' : city,
            'appid' : api_key,
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        return data

    # handle the get request which here is displaying the city search input
    def get(self, request):
        form = CityForm()
        return render(request, 'weather.html', {'form': form})


    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = self.get_weather(city)
            WeatherInfo.objects.update_or_create(user=request.user, defaults={'city': city})
            context = {
                'weather_data': weather_data,
                'form': form,
            }
            return render(request, 'weather.html', context)




class WeatherResultsView(LoginRequiredMixin, View):
    template_name = 'weather_results.html'

    def get_weather(self, city):
        api_key = settings.OPENWEATHER_API_KEY
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q' : city,
            'appid' : api_key,
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        return data

    def get(self, request, city):
        weather_data = self.get_weather(city)
        return render(request, self.template_name, {'weather_data': weather_data})




class WeatherAPIView(APIView):

    def get_weather(self, city):
        api_key = settings.OPENWEATHER_API_KEY
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q' : city,
            'appid' : api_key,
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        return data

    def get(self, request):
        form = CityForm()
        return Response({'form': form.data})

    def post(self, request):
        form = CityForm(request.data)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = self.get_weather(city)
            WeatherInfo.objects.update_or_create(user=request.user, defaults={'city': city})
            return Response({'weather_data': weather_data, 'form': form.data})
        return Response(form.errors, status=400)


class WeatherResultsAPIView(APIView):

    def get_weather(self, city):
        api_key = settings.OPENWEATHER_API_KEY
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q' : city,
            'appid' : api_key,
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        return data

    def get(self, request, city):
        weather_data = self.get_weather(city)
        return Response({'weather_data': weather_data})