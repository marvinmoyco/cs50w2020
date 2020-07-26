from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry_title):
    return render(request,"encyclopedia/entry.html",{
        "entry": util.get_entry(entry_title),
        "entry_str": entry_title.capitalize()
    })