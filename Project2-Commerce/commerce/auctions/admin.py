from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
# admin.site.register(Watchlist)
admin.site.register(Categories)
admin.site.register(Bid)