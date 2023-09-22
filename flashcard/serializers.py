from .models import *
from rest_framework import serializers




class FlashcardCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = FlashcardCategory
		fields = "__all__"



class FlashcardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flashcard
		fields = "__all__"