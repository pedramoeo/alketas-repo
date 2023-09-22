from .models import WeatherInfo
from rest_framework import serializers



class WeatherInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = WeatherInfo
		fields = "__all__"