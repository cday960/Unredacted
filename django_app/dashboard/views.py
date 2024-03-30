import requests
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django_htmx.middleware import HtmxDetails

from .models import Document, DigitalObject
from .atlas_connector import get_recent_docs, get_search_results, get_document, get_pdf 


ATLAS_URLS: dict[str, str] = {
    "process_naid": "http://127.0.0.1:5000/atlas/process",
    "search_docs": "http://127.0.0.1:5000/atlas/query",
    'recent_docs': "http://127.0.0.1:5000/atlas/recent",
    'pdf': "http://127.0.0.1:5000/atlas/pdf",
}
ATLAS_HEADERS = {"Content-Type": "application/json"}


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


@require_GET
def get_home_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    recent_docs: list[Document] = get_recent_docs(5)
    template = "home_page.html"
    context = {"test": "Home page switch", "data": {"recent_docs": recent_docs}}

    return render(request, template, context=context)


@require_GET
def get_search_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    return render(
        request, "search_page.html", context={"test": "Search Page Switch"}
    )


@require_GET
def get_about_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    return render(
        request, "about_page.html", context={"test": "About page switch"}
    )


@require_GET
def get_back_index(request: HtmxHttpRequest) -> HttpResponse:
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# searching for a document
@require_POST
def search_results_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)

    # filter query...maybe move somewhere else?
    search_query = str(request.POST.get("search_query")).replace(' ', '+')

    if len(search_query) > 1:

        # get the results from atlas
        search_results: list[Document] = get_search_results(search_query)

        return render(
            request,
            "search_results.html",
            context={
                "test": "document search results",
                "data": {
                    "search_results": search_results,
                    "search_query": search_query,
                },
            },
        )
    else:
        return get_search_index(request)


@require_GET
def display_doc_index(request: HtmxHttpRequest, naId: int) -> HttpResponse:
    print(request.htmx.trigger)
    document: Document = get_document(naId)
    print(document.to_dict())
    return render(
        request,
        "document_page.html",
        context={
            "test": f"Document load: naId = {document.naId}",
            "data": {"document": document.to_dict()},
        },
    )


@require_GET
def show_pdf(request: HtmxHttpRequest, url: str) -> HttpResponse:
    pdf_content = get_pdf(url)
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="document.pdf"'
    return response


@require_GET
def download_pdf(request: HtmxHttpRequest, url: str) -> HttpResponse:
    pdf_content = get_pdf(url)
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="document.pdf"'
    return response
