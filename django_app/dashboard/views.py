<<<<<<< HEAD

=======
import requests
>>>>>>> 82068427c0fc0d5cc49ca6181db6eae69d1f4d4f
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, FileResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
<<<<<<< HEAD
from .models import PageInfo, PageContext

from django_htmx.middleware import HtmxDetails

from utils import load_doc, get_doc_list_from_na, get_raw_na_url
from doc_models import Document


page_info: PageInfo = PageInfo(
    render="home_page.html",
    context=PageContext(test="Initial landing", title="Welcome to Unredacted"),
)
=======
from .models import Document, PageInfo, PageContext

from django_htmx.middleware import HtmxDetails

>>>>>>> 82068427c0fc0d5cc49ca6181db6eae69d1f4d4f

page_info: PageInfo = PageInfo(render="home_page.html", context=PageContext(test="Initial landing", title="Welcome to Unredacted"))

class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails
<<<<<<< HEAD


=======
    
>>>>>>> 82068427c0fc0d5cc49ca6181db6eae69d1f4d4f
# basic page display navigation, no arguments
@require_GET
def get_index(request: HtmxHttpRequest) -> HttpResponse:
    # this shows the trigger event in the django server terminal
    print(request.htmx.trigger)
    global page_info
    if request.htmx.trigger == "home_page_button":
<<<<<<< HEAD
        page_info.set_render_context(
            render="home_page.html",
            context=PageContext(test="Home Page Switch", title="Home"),
        )
    elif request.htmx.trigger == "search_page_button":
        page_info.set_render_context(
            render="search_page.html",
            context=PageContext(test="Search Page Switch", title="Search"),
        )
=======
        page_info.set_render_context(render="home_page.html", context=PageContext(test="Home Page Switch", title="Home"))
    elif request.htmx.trigger == "search_page_button":
        page_info.set_render_context(render="search_page.html", context=PageContext(test="Search Page Switch", title="Search"))
>>>>>>> 82068427c0fc0d5cc49ca6181db6eae69d1f4d4f
    elif request.htmx.trigger == "back_button":
        page_info.revert()
    else:
        page_info.set_render("landing_page.html")
        page_info.previous_render = "home_page.html"
<<<<<<< HEAD
        page_info.set_context(
            PageContext(test="Initial landing", title="Welcome to Unredacted")
        )

    return render(request, *page_info.get_render_context_dict())


=======
        page_info.set_context(PageContext(test="Initial landing", title="Welcome to Unredacted"))
    
    return render(request, *page_info.get_render_context_dict()) 

>>>>>>> 82068427c0fc0d5cc49ca6181db6eae69d1f4d4f
# searching for a document
@require_POST
def search_docs_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    if request.htmx.trigger == "document_search_button":
<<<<<<< HEAD
        search_query = str(request.POST.get("search_query"))
        if(len(search_query) > 1):
            search_results = get_doc_list_from_na(search_query)
            page_info.set_render_context(
                render="search_results.html",
                context=PageContext(
                    test="document search results",
                    title=f"Search results for '{search_query}'",
                    data={"search_results": search_results, "search_query": search_query},
                ),
            )
    return render(request, *page_info.get_render_context_dict())


@require_GET
def display_doc_index(request: HtmxHttpRequest, naId: int) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    if request.htmx.trigger == "document_page_button":
        document: Document = load_doc(naId)
        page_info.set_render_context(
            render="document_page.html",
            context=PageContext(
                test=f"Document load: naId = {document.naId}",
                title=f"{document.title}",
                data={"document": document},
            ),
        )
    return render(request, *page_info.get_render_context_dict())


@require_GET
def show_pdf(request: HtmxHttpRequest, url: str) -> HttpResponse:
    pdf_content = get_raw_na_url(url).content
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="document.pdf"'
    return response

@require_GET
def download_pdf(request: HtmxHttpRequest, url: str) -> HttpResponse:
    pdf_content = get_raw_na_url(url).content
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="document.pdf"'
    return response
=======
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
>>>>>>> 82068427c0fc0d5cc49ca6181db6eae69d1f4d4f
