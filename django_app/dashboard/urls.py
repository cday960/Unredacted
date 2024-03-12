from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.get_index, name="get_index"),
    path("search/", views.search_docs_index, name="search_docs_index"),
    path("display/<int:naId>/<str:title>/", views.display_doc_index, name="display_doc_index"),
]
