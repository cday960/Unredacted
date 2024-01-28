from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET

from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# # Create your views here.
# @require_GET
# def index(request: HtmxHttpRequest) -> HttpResponse:
#     # this shows the trigger event in the django server terminal
#     print(request.htmx.trigger)
#     if request.htmx.trigger == "replace_button":
#         context = {"test": "Button pressed!"}
#         # this entire html file is returned and placed into the target of the call
#         return render(request, "components/_partial.html", context)
#     else:
#         context = {"test": "Initial page load"}
#         return render(request, "dashboard/index.html", context)
    
# Create your views here.
@require_GET
def index(request: HtmxHttpRequest) -> HttpResponse:
    # this shows the trigger event in the django server terminal
    print(request.htmx.trigger)
    if request.htmx.trigger == "home_page_button":
        context = {"test": "Home Page Switch", "title": "Home"}
        return render(request, "home_page.html", context)
    elif request.htmx.trigger == "search_page_button":
        context = {"test": "Search Page Switch", "title": "Search"}
        return render(request, "search_page.html", context)
    elif request.htmx.trigger == "document_search_button":
        context = {"test": "document search results", "title": "Document Search Results Page"}
        return render(request, "search_results.html", context)
    elif request.htmx.trigger == "document_page_button":
        context = {"test": "document search", "title": "Document Page"}
        return render(request, "document_page.html", context)
    else:
        # landing page
        context = {"test": "Initial landing", "title": "Welcome to Unredacted"}
        return render(request, "landing_page.html", context)
