from django.urls import path
from django.conf.urls.static import static
from . import views
app_name = "auction"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing",views.add_listing, name="add_listing"),
    path("listing/<str:listing_name>",views.listing, name="listing")
]
