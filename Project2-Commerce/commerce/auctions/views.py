from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import *
import datetime
class New_Listing(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    initial_bid = forms.IntegerField(min_value=0)
    img_url = forms.URLField()
    categories = forms.CharField()

class New_Bid(forms.Form):
    new_bid = forms.IntegerField(min_value=0)

class New_Comment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

def index(request):
    
    return render(request, "auctions/index.html",{
        "active_listings": Listing.objects.all(),
        "active_bids": Bid.objects.all(),
        "index_active":True
    })

@login_required
def add_listing(request):
    new_listing = New_Listing()
    if request.method == "POST":
        new_listing = New_Listing(request.POST)
        if new_listing.is_valid():
            saved_categories = new_listing.cleaned_data["categories"]
            categories = saved_categories.split(",")

            save_listing = Listing(title=new_listing.cleaned_data["title"],description=new_listing.cleaned_data["description"],url=new_listing.cleaned_data["img_url"],creator=request.user,categories=saved_categories)
            save_listing.save()
            bid = Bid(bid = int(new_listing.cleaned_data["initial_bid"]),user=request.user)
            # save() is needed before adding a many to many relationship field
            bid.save() 
            bid.listing.add(save_listing)
            bid.save()
            for x in categories:
                try:
                    each_categ = Categories(categories=x)
                    each_categ.save()
                except IntegrityError:
                    break
            return HttpResponseRedirect(reverse('auction:index'))
    else:
        return render(request,"auctions/create.html",{
            "form":new_listing,
            "add_listing_active":True
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auction:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html",{
            "login_active":True
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auction:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auction:index"))
    else:
        return render(request, "auctions/register.html",{
            "register_active":True
        })

def listing(request,listing_name):
    current_listing = Listing.objects.get(title = listing_name)
    current_bid = Bid.objects.get(listing=current_listing)
    comment = Comment.objects.filter(listing=current_listing)
    new_comment1 = New_Comment()
    new_bid1 = New_Bid()
    if request.method == "POST":
        # When the form submitted is a comment form
        if 'comment_add' in request.POST:
            new_comment = New_Comment(request.POST)
            if new_comment.is_valid():
                text_comment = new_comment.cleaned_data["comment"]
                save_comment = Comment(username=request.user,comment=text_comment)
                save_comment.save()
                save_comment.listing.add(current_listing)

        # When the form submitted is a update bid form
        elif 'bid_add' in request.POST:
            new_bid = New_Bid(request.POST)
            if new_bid.is_valid():
                if new_bid.cleaned_data["new_bid"] > current_bid.bid:
                    Bid.objects.filter(listing=current_listing).update(bid=int(new_bid.cleaned_data["new_bid"]),user=request.user,date=datetime.datetime.now())
                    return render(request, "auctions/listing.html",{
                        "current_listing":current_listing,
                        "current_bid": current_bid,
                        "comments": comment,
                        "comment_form": new_comment1,
                        "bid_form": new_bid,
                        "message": "The bid is successfully updated!"

                    })
                else:
                    return render(request, "auctions/listing.html",{
                        "current_listing":current_listing,
                        "current_bid": current_bid,
                        "comments": comment,
                        "comment_form": new_comment1,
                        "bid_form": new_bid,
                        "message": "The bid should be higher than the current bid."

                    })
        # When the listing is added to the user's Watchlist
        elif 'watchlist_add' in request.POST:
            list_watchlist = Watchlist.objects.filter(user=request.user)
            try:
                list_watchlist.get(listing=current_listing)
            except Watchlist.DoesNotExist:
                new_watchlist = Watchlist()
                new_watchlist.save()
                new_watchlist.user.add(request.user)
                new_watchlist.listing.add(current_listing)
                return render(request, "auctions/listing.html",{
                "current_listing":current_listing,
                "current_bid": current_bid,
                "comments": comment,
                "comment_form": new_comment1,
                "bid_form": new_bid1,
                "message": "The listing is successfully added to your watchlist"
                })
            return render(request, "auctions/listing.html",{
                "current_listing":current_listing,
                "current_bid": current_bid,
                "comments": comment,
                "comment_form": new_comment1,
                "bid_form": new_bid1,
                "message": "The listing is already in the watchlist"
            })   
            
          

    return render(request, "auctions/listing.html",{
        "current_listing":current_listing,
        "current_bid": current_bid,
        "comments": comment,
        "comment_form": new_comment1,
        "bid_form": new_bid1,
        "message": None

    })