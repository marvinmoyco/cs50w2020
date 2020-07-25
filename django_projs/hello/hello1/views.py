from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello")

def marvin(request):
    return HttpResponse("Hello, Marvin")
