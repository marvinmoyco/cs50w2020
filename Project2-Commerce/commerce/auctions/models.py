from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.PositiveIntegerField(default=0)
    listing = models.ManyToManyField('Listing',blank=True,related_name="user_listing")
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User',blank=True,on_delete=models.CASCADE,related_name="current_bidder",default=None)

 
class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 256)
    description = models.TextField()
    url = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    categories = models.CharField(max_length=256,blank=True)
    bid_winner = models.ForeignKey('User',null=True,blank=True,on_delete=models.CASCADE,related_name="winner",default=None)
    creator = models.ForeignKey('User',on_delete=models.CASCADE,related_name="creator_listing",default=None)
    closed = models.IntegerField(default = 0)
    

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey('User',on_delete=models.CASCADE,related_name = "user_comment",default=None)
    comment = models.TextField(default="")
    comment_date = models.DateTimeField(auto_now=True)
    listing = models.ManyToManyField('Listing',blank=True,related_name="comment",default=None)
    
class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    categories = models.TextField(default="",unique=True,blank=True,null=True)

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ManyToManyField('User', blank=True, related_name="user_watchlist",default=None)
    listing = models.ManyToManyField('Listing',blank=True,related_name="watchlist",default=None)