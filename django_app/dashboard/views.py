import requests
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from .models import Document, PageInfo, PageContext

from django_htmx.middleware import HtmxDetails


page_info: PageInfo = PageInfo(render="home_page.html", context=PageContext(test="Initial landing", title="Welcome to Unredacted"))

class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails
    
# basic page display navigation, no arguments
@require_GET
def get_index(request: HtmxHttpRequest) -> HttpResponse:
    # this shows the trigger event in the django server terminal
    print(request.htmx.trigger)
    global page_info
    if request.htmx.trigger == "home_page_button":
        page_info.set_render_context(render="home_page.html", context=PageContext(test="Home Page Switch", title="Home"))
    elif request.htmx.trigger == "search_page_button":
        page_info.set_render_context(render="search_page.html", context=PageContext(test="Search Page Switch", title="Search"))
    elif request.htmx.trigger == "back_button":
        page_info.revert()
    else:
        page_info.set_render("landing_page.html")
        page_info.previous_render = "home_page.html"
        page_info.set_context(PageContext(test="Initial landing", title="Welcome to Unredacted"))
    
    return render(request, *page_info.get_render_context_dict()) 

# searching for a document
@require_POST
def search_docs_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    if request.htmx.trigger == "document_search_button":
        search_query: str = str(request.POST.get('search_query')).replace(' ', '+')
        # # process the request through the API
        # url = f"127.0.0.1:5000/webapp/search/{search_query}"
        # response = requests.get(url)
        # search_results: list[Document] = response.json()
        search_results = [Document(title=search_query, naId=5)]
        page_info.set_render_context(render="search_results.html", context=PageContext(test="document search results", title="Document Search Results Page", data={"search_results": search_results, "search_query": search_query}))
    return render(request, *page_info.get_render_context_dict()) 

@require_GET
def display_doc_index(request: HtmxHttpRequest, naId: int, title: str) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    if request.htmx.trigger == "document_page_button":
        # url = f"127.0.0.1:5000/webapp/search/{search_query}"
        # response = requests.get(url)
        # document: Document = response.to_dict[1]
        document : Document = Document(title=title, naId=naId)
        page_info.set_render_context(render="document_page.html", context=PageContext(test=f"Individual document load: naId = {document.naId}", title=f"Viewing {document.title}", data={"document": document}))
    return render(request, *page_info.get_render_context_dict()) 