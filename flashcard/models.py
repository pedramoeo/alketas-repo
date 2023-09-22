from django.db import models
from account.models import CustomUser




# Create your models here.
class FlashcardCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    category_name = models.CharField(max_length=50)
    language = models.CharField(max_length=10, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False, blank=True, null=True)


class Flashcard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(FlashcardCategory, on_delete=models.CASCADE, blank=True, null=True)
    front = models.TextField()
    back = models.TextField()
    is_pinned = models.BooleanField(default=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
