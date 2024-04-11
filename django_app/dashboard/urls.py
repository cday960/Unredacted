from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.get_home_index, name="landing_index"),
    path("home/", views.get_home_index, name="home_index"),
    path("search/", views.get_search_index, name="search_index"),
    path("about/", views.get_about_index, name="about_index"),
    path("back/", views.get_back_index, name="back_index"),
    path("api_info/", views.get_api_info_index, name="api_info_index"),
    path("search_results/", views.search_results_index, name="search_results_index"),
    path("display/<int:naId>/", views.display_doc_index, name="display_doc_index"),
    path("show_pdf/<path:url>/", views.show_pdf, name="show_pdf"),
    path("download_pdf/<path:url>/", views.download_pdf, name="download_pdf"),
]
