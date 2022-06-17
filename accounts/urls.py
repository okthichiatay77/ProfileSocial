from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('edit/', edit_profile, name='edit'),
    path('user/<username>/', user, name='user'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('follow/<username>/', follow, name='follow'),
    path('unfollow/<username>/', un_follow, name='unfollow'),
    path('list-friend/', list_add_friend, name='list_friends')
]