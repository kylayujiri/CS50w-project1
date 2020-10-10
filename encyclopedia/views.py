import markdown2
import random

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title", required=True)
    md_text = forms.CharField(label="Markdown Content", widget=forms.Textarea, required=True)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    unconverted = util.get_entry(title)
    if unconverted is None:
        return render(request, "encyclopedia/not-found.html", {
            "title": title
        })
    html = markdown2.markdown(unconverted)
    # the html gets returned as a string so I will have to make an entry.html after all
    # then we will have to send the string in the context of the render and display it
    # we will need to keep in mind the safe filter
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "html": html
    })

def search(request):
    if request.method == "POST":
        query = request.POST.get('q')

        partial_matches = []

        for entry in util.list_entries():
            if query.lower() == entry.lower(): # the search terms matches an encyclopedia entry exactly
                return HttpResponseRedirect(reverse('encyclopedia:entry', args=[query]))
            elif query.lower() in entry.lower(): # look for partial matches in case there are no exact matches
                partial_matches.append(entry)

        return render(request, "encyclopedia/search-results.html", {
            "query": query,
            "results": partial_matches
        })

    else:
        return HttpResponseRedirect(reverse('encyclopedia:index'))

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        error = ""

        if form.is_valid():
            title = form.cleaned_data["title"]
            md_text = form.cleaned_data["md_text"]

            if util.get_entry(title) is None:

                util.save_entry(title, md_text)

                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

            else:

                error = "An entry with that title already exists."

        return render(request, "encyclopedia/new-page.html", {
            "form": form,
            "error": error
        })

    else:
        return render(request, "encyclopedia/new-page.html", {
            "form": NewPageForm
        })

def edit(request, title):

    if request.method == "POST":

        form = NewPageForm(request.POST)

        if form.is_valid():
            md_text = form.cleaned_data["md_text"]

            util.save_entry(title, md_text)

            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))

        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })

    else:
        form = NewPageForm(initial={"title": title, "md_text": util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })

def random_page(request):
    page = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[page]))
