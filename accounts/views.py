from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User


from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from .tokens import account_activation_token
from .forms import *
from .models import UserProfile, Follow

from posts.forms import CreatePost
# Create your views here.




def signup_view(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(request.POST)

        if form.is_valid():
            user = form.save()
            user_profile = UserProfile(user = user)
            user_profile.save()

            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')


    return render(request, 'accounts/signup.html', context={'form':form, 'title':'Sign Up Form Here', 'registered':registered})


def login_view(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'accounts/login.html', {'title':'Login Page','form':form})


@login_required
def profile_view(request):
    form = CreatePost()
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('posts:index'))
    return render(request, 'accounts/profile.html', context={'form':form})


@login_required
def edit_profile(request):
    current_user = request.user
    profile = UserProfile.objects.get(user= current_user)
    form = EditProfile(instance=profile)

    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=profile)
            return HttpResponseRedirect(reverse('accounts:profile'))


    return render(request, 'accounts/edit_profile.html', context={'form':form, 'current_user':current_user})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('posts:index'))


@login_required
def user(request, username):
    user = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user)
    if user == request.user:
        return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/user_other.html', {'user':user, 'already_followed':already_followed})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)

    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()

    return HttpResponseRedirect(reverse('accounts:user', kwargs={'username':username}))

@login_required
def un_follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('accounts:user', kwargs={'username':username}))