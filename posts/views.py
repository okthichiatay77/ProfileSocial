from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


from .models import Post, Like, Comment
from accounts.models import Follow, UserProfile
from .forms import CommentForm, CreatePost


def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', context={'posts':posts})

@login_required
def list_post(request):
    following_list = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=following_list.values_list('following'))

    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)

    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = User.objects.filter(username__icontains=search)


    return render(request, 'posts/list_post.html', {'search':search, 'result':result, 'posts':posts, 'liked_post_list':liked_post_list})


@login_required
def liked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)

    if not already_liked:
        like_post = Like(post=post, user=request.user)
        like_post.save()

    return HttpResponseRedirect(reverse('posts:index'))


@login_required
def unliked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('posts:index'))


def detail_post(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        content = request.POST['content']
        comment = Comment.objects.create(post=post, user=request.user, content=content)
        comment.save()
        return HttpResponseRedirect(reverse('posts:detail_post', kwargs={'pk':pk}))

    return render(request, 'posts/detail_post.html', context={'post':post,'comments':comments})

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    form = CreatePost(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'posts/update_post.html', {'form':form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()

        return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'posts/delete_post.html')

