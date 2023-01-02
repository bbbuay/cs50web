from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # adding path to new page (/new)
    path("new", views.new_page, name="new"),
    # adding path to random page (/random)
    path("random", views.random_page, name="random"),
    # adding path to search page (/search)
    path("search", views.search_page, name="search"),
    # adding path to entry page (/title)
    path("<str:title>", views.entry_page, name="entry"),
    #adding path to edit page (/edit)
    path("<str:title>/edit", views.edit_page, name="edit"),
]
