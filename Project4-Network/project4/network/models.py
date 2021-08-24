from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    followers = models.ManyToManyField("User",related_name='supporter')
    following = models.ManyToManyField("User",related_name='user_follow')
    posts = models.ForeignKey("User", on_delete=models.CASCADE,default=None, related_name="user_posts")


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts_user")
    content = models.TextField(blank=True,null=True,max_length=480)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField("User", related_name="likes_in_post",default=None)