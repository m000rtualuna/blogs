from django.db import models
from django.contrib.auth.models import AbstractUser
from blogs import settings


class MyUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    bio = models.TextField()

class Post(models.Model):
    MyUser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post_content = models.TextField(default='')
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)

class Comment(models.Model):
    comment_text = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)