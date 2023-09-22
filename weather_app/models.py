from django.db import models
from account.models import CustomUser



# Create your models here.
class WeatherInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=50, blank=True, null=True)

    # this method overrides the city field and set it to user.city as long as
    # it's not been inputed by the user
    def save(self, *args, **kwargs):
        if not self.pk:
            self.city_name = self.user.city
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username}'s {self.city_name}"
