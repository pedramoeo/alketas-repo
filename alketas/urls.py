from django.contrib import admin
from django.urls import path, include





urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('account.urls')),
    path('', include('weather_app.urls')),
    path('', include('to_do_list.urls')),
    path('', include('flashcard.urls')),
    path('', include('pages.urls')),

]
