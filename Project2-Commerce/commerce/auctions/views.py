from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Listing
class New_Listing(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    initial_bid = forms.IntegerField(min_value=0)
    img_url = forms.URLField()
    categories = forms.CharField()



def index(request):
    
    return render(request, "auctions/index.html",{
        "active_listings": Listing.objects.all(),
        "index_active":True
    })

def add_listing(request):
    new_listing = New_Listing()
    if request.method == "POST":
        new_listing = New_Listing(request.POST)
        if new_listing.is_valid():
  
            save_listing = Listing(title=new_listing.cleaned_data["title"],description=new_listing.cleaned_data["description"],url=new_listing.cleaned_data["img_url"],initial_bid=new_listing.cleaned_data["initial_bid"])
            save_listing.save()
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


    return render(request, "auctions/listing.html",{
        "current_listing":current_listing
    })