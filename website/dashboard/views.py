from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

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
    
previous_render = "home_page.html"
previous_context: dict[str, str] = {"test": "Initial landing", "title": "Welcome to Unredacted"}

@require_GET
def get_index(request: HtmxHttpRequest) -> HttpResponse:
    # this shows the trigger event in the django server terminal
    print(request.htmx.trigger)
    global previous_context
    global previous_render
    if request.htmx.trigger == "home_page_button":
        context = previous_context = {"test": "Home Page Switch", "title": "Home"}
        new_render = previous_render = "home_page.html"
    elif request.htmx.trigger == "search_page_button":
        context = previous_context = {"test": "Search Page Switch", "title": "Search"}
        new_render = previous_render = "search_page.html"
    # elif request.htmx.trigger == "document_search_button":
    #     context = previous_context = {"test": "document search results", "title": "Document Search Results Page"}
    #     new_render = previous_render = "search_results.html"
    elif request.htmx.trigger == "document_page_button":
        # uses back button, so do not set previous context/render
        context = {"test": "document search", "title": "Document Page"}
        new_render = "document_page.html"
    elif request.htmx.trigger == "back_button":
        context = previous_context
        new_render = previous_render
    else:
        # landing page
        context = previous_context = {"test": "Initial landing", "title": "Welcome to Unredacted"}
        new_render = "landing_page.html"
        previous_render = "home_page.html"
    
    return render(request, new_render, context) 

@require_POST
def search_index(request: HtmxHttpRequest) -> HttpResponse:
    global previous_context
    global previous_render
    if request.htmx.trigger == "document_search_button":
        search_query: str = request.POST.get('search_query')
        # process the request through the API
        # search_results: dict[str, list[str: str]] = api.get_search_results(search_query)
        search_results: list[dict[str, str]] = [{"id": "001", "name": "name_doc_1", "details": "test doc 1 details", "original_date": "01/01/2001", "posted_date": "01/12/2024"}]
        context = previous_context = {"test": "document search results", "title": "Document Search Results Page", "search_results": search_results, "search_query": search_query}
        new_render = previous_render = "search_results.html"
    return render(request, new_render, context) 