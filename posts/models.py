from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=200, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-upload_date',]

    def count_liked(self):
        return self.liked_post.count()

    def count_comments(self):
        return self.post_comment.count()



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    content = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user

    def count_like_comment(self):
        return self.liked_comment.count()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_liked')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.user, self.post)

class LikeOfComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='liked_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_liked_commet')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.user, self.comment)

