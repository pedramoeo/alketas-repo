from django.views import View
from django.shortcuts import render, redirect 
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

from .models import *
from .forms import CityForm

from django.conf import settings










class WeatherView(View):

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
        return render(request, 'weather.html', {'form': form})

    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = self.get_weather(city)
            WeatherInfo.objects.update_or_create(user=request.user, defaults={'city_name': city})
            request.session['weather_data'] = weather_data  # Save data in session
            return redirect('weather-results', city=city)  # Redirect to a new view
        else:
            return render(request, 'weather.html', {'form': form})



class WeatherResultsView(View):

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
        form = CityForm()
        weather_data = self.get_weather(city)
        return render(request, 'weather-results.html', {'form': form, 'weather_data': weather_data})
    
    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = self.get_weather(city)
            WeatherInfo.objects.update_or_create(user=request.user, defaults={'city_name': city})
            request.session['weather_data'] = weather_data  # Save data in session
            return redirect('weather-results', city=city)  # Redirect to a new view
        else:
            return render(request, 'weather.html', {'form': form})