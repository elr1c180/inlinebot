from django.urls import path
from .views import *

urlpatterns = [
    path('', all_art, name="all"),
    path('create/', create, name='create'),
    path('success/', success, name='success')
]