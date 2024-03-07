from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.get_index, name="get_index"),
    path("search/", views.search_index, name="search_index"),
]
