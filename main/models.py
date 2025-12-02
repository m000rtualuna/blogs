from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    bio = models.TextField()

class Post(models.Model):
    MyUser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post_content = models.TextField(default='')
    pub_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment_text = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    my_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')