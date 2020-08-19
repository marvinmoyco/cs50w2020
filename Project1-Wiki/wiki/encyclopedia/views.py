from django.shortcuts import render
from django.http import HttpResponseRedirect,QueryDict
from django.urls import reverse
from . import util
import random
from markdown2 import Markdown
from django import forms

#This class if only used for the edit page since it will surely have a title
class Edit_EntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
# This class is form adding new entries so it has a title and content
class Add_EntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

# The index function is simple since it only needs to pass the list of entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#The entry page displays the entry selected and converts markdown to html tags
def entry(request,entry_title):
    str1 = entry_title.lower()
    markdowner = Markdown()     #Sets up the markdown object
    for str2 in util.list_entries():    #This forloop checks the input string matches any of the entries in the list
        str2 = str2.lower()
        check_str = str1.find(str2,0,len(str2))
        if check_str >= 0:
            break

    if check_str == -1:                 #Show error page if there is no match
        return render(request,"encyclopedia/entry_error.html",{
            "entry_str": entry_title
        })
    elif check_str == 0:
       if util.get_entry(entry_title) is None:  
            return render(request,"encyclopedia/entry_error.html",{
                "entry_str": entry_title
            })
    return render(request,"encyclopedia/entry.html",{   #Show the entry page is it is a match and convert markdown to html
         "entry": markdowner.convert(util.get_entry(entry_title)),
        "entry_str": entry_title
    })

def add_entry(request):     
    empty_form = Add_EntryForm()
    if request.method == "POST":
        new_entry = Add_EntryForm(request.POST)
        if new_entry.is_valid():
            new_title = new_entry.cleaned_data["title"] #IMPORTANT: convert the data to .cleaned_data so it can be saved
            new_content = new_entry.cleaned_data["content"]
            if new_title in util.list_entries():        #Checks if there is already a existing entry with the same title
                return render(request, "encyclopedia/add_error.html",{
                    "entry_str":new_title
                })
            else:
                util.save_entry(new_title,new_content)
                return HttpResponseRedirect(reverse("wiki:entry",args=[new_title])) #Redirect to the new entry after creating it
    return render(request, "encyclopedia/add_entry.html",{
        "form":empty_form
    })

def edit_entry(request, entry_obj):
    initial_form = Edit_EntryForm(initial={'title':entry_obj,'content':util.get_entry(entry_obj)})  #Puts the initial value to be edited on the edit page
    if request.method == "POST":
        entry_edit = Edit_EntryForm(request.POST)
        if entry_edit.is_valid():
            content_saved = entry_edit.cleaned_data["content"]  #IMPORTANT AGAIN: convert it using .cleaned_data["attribute"]
            util.save_entry(entry_obj,content_saved)
            return HttpResponseRedirect(reverse("wiki:entry",args=[entry_obj]))  #Redirect to the edited entry page to see the entry
    
    if entry_obj in util.list_entries():        #Shows the initial values in the page
        return render(request, "encyclopedia/edit_entry.html",{
            "entry_str": entry_obj,
            "entry": util.get_entry(entry_obj),
            "form": initial_form
        })
    else:
        return render(request,"encyclopedia/entry_error.html",{ #Error page in case there is no entry with the same string
            "entry_str":entry_obj
        })
    

def random_entry(request):      #Uses random lib of python and maps it into an entry in the list (using the index)
    len_entries = len(util.list_entries())
    len_entries -= 1
    ran_num = random.randint(0,len_entries)
    ran_entry = util.list_entries()
    return HttpResponseRedirect(reverse("wiki:entry", args=[ran_entry[ran_num]]))


def search_entry(request):  
    search_q = request.GET.get('q')     #Used .get() to get the GET parameter needed (in this case, 'q' parameter)
    search_q = search_q.strip()
    buf2 = search_q.lower()
    lower_entries = []
    check = False
    for buf in util.list_entries():     #Triple nested for loop checks every character in the string of every entry for a match
        buf1 = buf.lower()
        for x in range(len(search_q)):
            for y in range(len(buf)):
                check = buf2[x] == buf1[y]      #Checks if there is a matching character
                if check == True:
                    lower_entries.append(buf)   #If there is, then append it to an empty list
                    break
            if check == True:                   #Used to prevent duplicate appends
                check = False
                break
        

    if search_q in util.list_entries():         #Presents the result if there is a exact match
        return HttpResponseRedirect(reverse('wiki:entry',args=[search_q]))
    else:
        return render(request,"encyclopedia/search_entry.html",{    #If there is no exact match, send the list (of the possible entries) and the search query
            "query": search_q,
            "ref_entry": lower_entries
        })

