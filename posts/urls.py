from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', home, name='index'),
    path('list_post/', list_post, name='list_post'),
    path('liked/<int:pk>/', liked, name='liked'),
    path('unliked/<int:pk>/', unliked, name='unliked'),
    path('detail/<int:pk>/', detail_post, name='detail_post'),
    path('update/<int:pk>/', update_post, name='update_post'),
    path('delete/<int:pk>/', delete_post, name='delete_post'),
    #path('liked-comment/<int:pk>/', liked_comment, name='liked_comment'),
    #path('unliked-comment/<int:pk>/', unliked_comment, name='unliked_comment'),
]