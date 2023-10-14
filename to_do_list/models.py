from django.db import models
from account.models import CustomUser


# Create your models here.
class Category(models.Model):
    CATEGORY_COLOUR = (('blue', 'Blue'), ('red', 'Red'), ('green', 'Green'),
                       ('yellow', 'Yellow'), ('black', 'Black'), ('white', 'White'),
                       ('orange', 'Orange'), ('purple', 'Purple'), ('pink', 'Pink'),
                       ('grey', 'Grey'))
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True, blank=False, null=True)
    category_colour = models.CharField(max_length=6, choices=CATEGORY_COLOUR, default='white', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False, blank=True, null=True)
    slug = models.SlugField(max_length=200, null=True)

    
    def __str__(self) -> str:
        return self.category_name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'



class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=True)
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    is_complete = models.BooleanField(default=False, blank=True, null=True)
    is_pinned = models.BooleanField(default=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    due_time = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=200, null=True)

    class Meta:
        ordering = ['-is_pinned', '-is_complete', 'title', 'due_time']


    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        if self.category is not None:
            return f'/{self.category.slug}/{self.slug}/'
        else:
            return f'/{self.slug}/'

    