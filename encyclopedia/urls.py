from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("wiki", views.index, name="wiki"),
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new-page", views.new_page, name="new-page"),
    path("random", views.random_page, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit")
]
