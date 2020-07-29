from django.shortcuts import render
from django.http import HttpResponseRedirect,QueryDict
from django.urls import reverse
from . import util
import random
from markdown2 import Markdown
from django import forms

class Edit_EntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class Add_EntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry_title):
    str1 = entry_title.lower()
    markdowner = Markdown()
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
         "entry": markdowner.convert(util.get_entry(entry_title)),
        "entry_str": entry_title.upper()
    })

def add_entry(request):
    empty_form = Add_EntryForm()
    if request.method == "POST":
        new_entry = Add_EntryForm(request.POST)
        if new_entry.is_valid():
            new_title = new_entry.cleaned_data["title"]
            new_content = new_entry.cleaned_data["content"]
            if new_title in util.list_entries():
                return render(request, "encyclopedia/add_error.html",{
                    "entry_str":new_title
                })
            else:
                util.save_entry(new_title,new_content)
                return HttpResponseRedirect(reverse("wiki:entry",args=[new_title]))
    return render(request, "encyclopedia/add_entry.html",{
        "form":empty_form
    })

def edit_entry(request, entry_obj):
    initial_form = Edit_EntryForm(initial={'title':entry_obj,'content':util.get_entry(entry_obj)})
    if request.method == "POST":
        entry_edit = Edit_EntryForm(request.POST)
        if entry_edit.is_valid():
            content_saved = entry_edit.cleaned_data["content"]
            util.save_entry(entry_obj,content_saved)
            return HttpResponseRedirect(reverse("wiki:entry",args=[entry_obj]))  
    
    if entry_obj in util.list_entries():
        return render(request, "encyclopedia/edit_entry.html",{
            "entry_str": entry_obj,
            "entry": util.get_entry(entry_obj),
            "form": initial_form
        })
    else:
        return render(request,"encyclopedia/entry_error.html",{
            "entry_str":entry_obj.capitalize()
        })
    

def random_entry(request):
    len_entries = len(util.list_entries())
    len_entries -= 1
    ran_num = random.randint(0,len_entries)
    ran_entry = util.list_entries()
    return HttpResponseRedirect(reverse("wiki:entry", args=[ran_entry[ran_num]]))


def search_entry(request):
    search_q = request.GET.get('q')
    search_q = search_q.strip()
    buf2 = search_q.lower()
    lower_entries = []
    for buf in util.list_entries():
        buf1 = buf.lower()
        for x in range(len(search_q)):
            for y in range(len(buf)):
                if buf2[x] == buf1[y]:
                    lower_entries.append(buf)
                    break
        

    if search_q in util.list_entries():
        return HttpResponseRedirect(reverse('wiki:entry',args=[search_q]))
    else:
        return render(request,"encyclopedia/search_entry.html",{
            "query": search_q,
            "ref_entry": lower_entries
        })

