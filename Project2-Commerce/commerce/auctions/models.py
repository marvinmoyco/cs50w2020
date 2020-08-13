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
    title = models.CharField(max_length = 64)
    description = models.TextField()
    initial_bid = models.PositiveIntegerField()
    url = models.URLField()
    date_of_listing = models.DateTimeField(auto_now_add=True)
    #bid = models.ForeignKey('Bid' ,on_delete=models.CASCADE,related_name="current_bid",default=None)
    

class Comment(models.Model):
    username = models.ForeignKey('User',on_delete=models.CASCADE,related_name = "user",default=None)
    comment = models.TextField(default="")
    comment_date = models.DateTimeField(auto_now=True)
    listing = models.ManyToManyField('Listing',blank=True,related_name="listing")
    


    