from django.db import models
from account.models import CustomUser




# Create your models here.
class FlashcardCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)
    category_name = models.CharField(max_length=50)
    language = models.CharField(max_length=10, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False, blank=True, null=True)
    slug = models.SlugField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.category_name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Flashcard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(FlashcardCategory, on_delete=models.CASCADE, blank=True, null=True)
    front = models.TextField()
    back = models.TextField()
    is_pinned = models.BooleanField(default=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, null=True)

    def __str__(self):
        return self.front
    
    def get_absolute_url(self):
        if self.flashcardcategory is not None:
            return f'/{self.flashcardcategory}/{self.slug}/' 
        else:
            return f'/{self.slug}/'
