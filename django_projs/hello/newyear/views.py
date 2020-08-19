from django.shortcuts import render
import datetime
# Create your views here.
def index(request):
    now = datetime.datetime.now()
    now_bool = now.month == 1 and now.day == 1
    return render(request, "newyear/index.html", {
        "is_it_newyear": now_bool
    })