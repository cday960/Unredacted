from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.get_index, name="get_index"),
    path("search/", views.search_docs_index, name="search_docs_index"),
    path("display/<int:naId>/", views.display_doc_index, name="display_doc_index"),
    path("show_pdf/<path:url>/", views.show_pdf, name="show_pdf"),
    path("download_pdf/<path:url>/", views.download_pdf, name="download_pdf"),
]
