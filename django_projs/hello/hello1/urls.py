from . import views
from django.urls import path 
urlpatterns=[
    path("",views.index,name="index"),
    path("<str:str1>",views.greet, name="greet"),
    path("marvin",views.marvin,name="marvin")
]