from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, FileResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from .models import PageInfo, PageContext

from django_htmx.middleware import HtmxDetails

from utils import load_doc, get_doc_list_from_na, get_raw_na_url, get_recent_docs
from doc_models import Document


page_info: PageInfo = PageInfo(
    render="landing_page.html",
    context=PageContext(test="Initial landing", title="Welcome to Unredacted"),
    avoid_switch={"landing_page.html": "home_page.html"}
)


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def get_home_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    recent_docs = get_recent_docs(num_docs=5)
    if request.htmx.trigger == "home_page_button":
        page_info.set_render_context(
            render="home_page.html",
            context=PageContext(test="Home Page Switch", title="Home", data={'recent_docs': recent_docs}),
        )
    else:
        page_info.set_render_context(
            render="landing_page.html",
            context=PageContext(test="Initial landing", title="Welcome to Unredacted", data={'recent_docs': recent_docs}),
        )
        page_info.render = "landing_page.html"
    return render(request, *page_info.get_render_context_dict())


def get_search_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    page_info.set_render_context(
        render="search_page.html",
        context=PageContext(test="Search Page Switch", title="Search"),
    )
    return render(request, *page_info.get_render_context_dict())


def get_about_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    page_info.set_render_context(
        render="about_page.html",
        context=PageContext(test="About Page Switch", title="About Unredacted"),
    )
    return render(request, *page_info.get_render_context_dict())

def get_back_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    page_info.revert()
    return render(request, *page_info.get_render_context_dict())


# searching for a document
@require_POST
def search_results_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    search_query = str(request.POST.get("search_query"))
    if len(search_query) > 1:
        search_results = get_doc_list_from_na(search_query)
        page_info.set_render_context(
            render="search_results.html",
            context=PageContext(
                test="document search results",
                title=f"Search results for '{search_query}'",
                data={
                    "search_results": search_results,
                    "search_query": search_query,
                },
            ),
        )
    return render(request, *page_info.get_render_context_dict())


@require_GET
def display_doc_index(request: HtmxHttpRequest, naId: int) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
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
