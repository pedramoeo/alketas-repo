from django.db import models
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.models import AbstractUser, Group, Permission



# Create your models here.
class CustomUser(AbstractUser):
    city = models.CharField(max_length=12, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name= ('groups'),
        blank=True,
        help_text= (
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set",
        related_query_name="customuser",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name= ('user permissions'),
        blank=True,
        help_text= ('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    profile_picture = models.ImageField(default='static/profile-images/PROFILE.png', upload_to='static/profile-images', blank=True, null=True)


    



    def __str__(self):
        return self.user.username