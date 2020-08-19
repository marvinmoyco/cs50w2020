from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass
 
class Bid(models.Model):
    date = models.DateTimeField(auto_now=True)
    value = models.PositiveIntegerField(default=0)
    listing = models.ForeignKey('Listing',on_delete=models.CASCADE,related_name="listing_bid",default=None)

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 64)
    description = models.TextField()
    initial_bid = models.IntegerField(default=0)
    url = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Categories',blank=True,related_name="listing_categories")
    #bid = models.ForeignKey('Bid' ,on_delete=models.CASCADE,related_name="current_bid",default=None)
    

class Comment(models.Model):
    username = models.ForeignKey('User',on_delete=models.CASCADE,related_name = "user_comment",default=None)
    comment = models.TextField(default="")
    comment_date = models.DateTimeField(auto_now=True)
    listing = models.ManyToManyField('Listing',blank=True,related_name="comment")
    
class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    categories = models.TextField(default="")

    