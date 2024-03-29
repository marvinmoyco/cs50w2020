from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.utils import OperationalError

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    birthdate = models.DateField(blank=True, null=True, default=None)
    posts = models.ManyToManyField("Post",default=None,related_name="user_posts")
    creationDate = models.DateTimeField(auto_now_add=True)

    
    def serialize(self):
        posts = []

        for post in self.post_creator.order_by("-timestamp").all():
            posts.append(post.serialize())

        return{
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "followers": self.follower.all().count(),
            "posts": posts,
            "date_created": self.creationDate,

        }


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.PROTECT,related_name="post_creator")
    content = models.TextField(blank=True,null=True,max_length=480)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True,blank=True,null=True)
    likes = models.ManyToManyField("Liking",blank=True, related_name="likes_in_post",default=None)

    def serialize(self):
       
            
        return{
            "user": self.user.username,
            "content": self.content,
            "date_posted": self.timestamp.strftime("%x"),
            "date_edited": self.last_edited.strftime("%x %X"),
            "likes": self.liked_post.all().count(),
        }


class Following(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.PROTECT ,null=True, related_name="followed")
    following_user = models.ManyToManyField('User',related_name='follower')
    date_followed = models.DateTimeField(auto_now=True)


class Liking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.PROTECT,null=True, related_name="liker")
    post = models.ManyToManyField("Post",related_name="liked_post")
    date_liked = models.DateTimeField(auto_now=True)