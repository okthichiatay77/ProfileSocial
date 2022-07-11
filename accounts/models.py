from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

"""class User(AbstractUser):
    user_pic = models.ImageField(upload_to='user_pics', blank=True)
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    phone = models.IntegerField()"""


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    description = models.TextField(blank=True)
    full_name = models.CharField(max_length=200, blank=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
