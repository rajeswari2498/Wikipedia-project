from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import markdown2 as md

from . import util

# Create your views here.

class EntityForm(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request,"encyclopedia/index.html",{
        "entries" : util.list_entries()
    })

def g_content(request,title):
    try:
        content = util.get_entry(title)

        return render(request, "encyclopedia/wiki.html",{
            "title": title,
            "content": content
        })

    except:
        content = " please try again!"
        
        return render(request, "encyclopedia/wiki.html",{
            "title": title,
            "content": content,
            "message": "omg"
        })

def search(request):
    if request.method == "POST":
        search1 = request.POST.get("q", "")
        list1 = []
        if util.get_entry(search1):
            return g_content(request,search1)
        else:
            for i in util.list_entries():
                if search1.lower() == i[:len(search1)].lower():
                    list1.append(i)

    return render(request, "encyclopedia/search.html",{
        "list1": list1
    })


def create(request):
    if request.method == "POST":
        form = EntityForm(request.POST)
        message =""
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title)):
                message = "Sorry, this title already exists... Try something else."
                return render(request,"encyclopedia/create.html",{
                    "form":form,
                    "message":message
                })
            else:
                util.save_entry(title,content)
                return g_content(request,title)

        else:
            return render(request,"encyclopedia/create.html",{
                "form":form
            })

    return render(request, "encyclopedia/create.html",{
        "form": EntityForm()
    })

def edit(request):

    if request.method == "POST":
        form = EntityForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title,content)
            g_content(request,title)

        return g_content(request,title)
    
    else:
        return render(request,"encyclopedia/edit.html",{
            "message":"Something went wrong. Try again!",
            "form":form
        })

def initialize(request, title):
    InitialForm = EntityForm(initial={'title': title, 'content':util.get_entry(title)})
    return render(request,"encyclopedia/edit.html",{ 
        "form":InitialForm
    })

def random_e(request):
    allentries = util.list_entries()
    entry = random.choice(allentries)

    return render(request, "encyclopedia/wiki.html",{
        "title": entry,
        "content":util.get_entry(entry)
    })

def g_markdown(self):
    content = self.content
    return md(content)


    