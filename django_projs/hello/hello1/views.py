from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request,"hello1/index.html")

def marvin(request):
    return HttpResponse("Hello, Marvin")

def greet(request,str1):
    return render(request,"hello1/greet.html",{
        "name": str1.capitalize()
    })