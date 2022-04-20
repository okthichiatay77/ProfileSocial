from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', home, name='index'),
    path('list_post/', list_post, name='list_post'),
    path('liked/<int:pk>/', liked, name='liked'),
    path('unliked/<int:pk>/', unliked, name='unliked'),
]