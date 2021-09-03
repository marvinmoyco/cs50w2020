from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import *


def index(request):
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def profile(request,username):
    # Query for requested email
    try:
        user = User.objects.get(user=request.user)
    except User.DoesNotExist:
        return JsonResponse({"error": "User account not found."}, status=404)

    return JsonResponse(user.serialize(),safe=False)



@login_required
def news_feed(request):

    if request.method == "POST":
        data = json.loads(request.body)
        #Check if author exists
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return JsonResponse({"error":f"User account with username: {request.user} does not exist."},status=404)

        #Get the post content
        post_content = data.get("post_content")
        if post_content.strip() == "":
            return JsonResponse({"error":"Post should not be empty or whitespaces only."},status_code=404 )

        #Save the post in db

        post = Post(
                    author  = request.user,
                    content = post_content
                    )

        post.save()
        return JsonResponse({"message": "Post successfully posted"},status_code = 201)

    else:
        posts = Post.objects.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts ],safe=False)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
