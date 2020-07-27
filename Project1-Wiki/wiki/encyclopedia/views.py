from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry_title):
    str1 = entry_title.lower()
    for str2 in util.list_entries():
        str2 = str2.lower()
        check_str = str1.find(str2,0,len(str2))
        if check_str == 0:
            break

    if check_str == -1:
        return render(request,"encyclopedia/entry_error.html",{
            "entry_str": entry_title.capitalize()
        })
    elif check_str == 0:
        if util.get_entry(entry_title) is None:
            return render(request,"encyclopedia/entry_error.html",{
                "entry_str": entry_title.capitalize()
            })
        return render(request,"encyclopedia/entry.html",{
            "entry": util.get_entry(entry_title),
            "entry_str": entry_title.upper()
        })

def add_entry(request):
    return render(request, "encyclopedia/add_entry.html",{

    })

def edit_entry(request):
    return render(request, "encyclopedia/add_entry.html",{

    })

def random_entry(request):
    len_entries = len(util.list_entries())
    len_entries -= 1
    ran_num = random.randint(0,len_entries)
    ran_entry = util.list_entries()
    return HttpResponseRedirect(reverse("wiki:entry", args=[ran_entry[ran_num]]))
