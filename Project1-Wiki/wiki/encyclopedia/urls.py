from django.urls import path

from . import views
app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>",views.entry,name="entry"),
    path("add_entry",views.add_entry,name="add_entry"),
    path("edit/<str:entry_obj>",views.edit_entry,name="edit_entry"),
    path("random_entry",views.random_entry,name="random_entry")
]
