from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, FileResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from .models import PageInfo, PageContext

from django_htmx.middleware import HtmxDetails

from utils import load_doc
from doc_models import Document

import requests


page_info: PageInfo = PageInfo(
    render="home_page.html",
    context=PageContext(test="Initial landing", title="Welcome to Unredacted"),
)

page_info: PageInfo = PageInfo(
    render="home_page.html",
    context=PageContext(test="Initial landing", title="Welcome to Unredacted"),
)


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


atlas_url = "http://127.0.0.1:5000"
headers = {"Content-Type": "application/json"}


# basic page display navigation, no arguments
@require_GET
def get_index(request: HtmxHttpRequest) -> HttpResponse:
    # this shows the trigger event in the django server terminal
    print(request.htmx.trigger)
    global page_info

    if request.htmx.trigger == "home_page_button":
        return render(
            request, "home_page.html", {"test": "Home Page Switch", "title": "Home"}
        )
    elif request.htmx.trigger == "search_page_button":
        return render(
            request,
            "search_page.html",
            {"test": "Serach Page Switch", "title": "Search"},
        )
    elif request.htmx.trigger == "back_button":
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        return render(
            request,
            "landing_page.html",
            {"test": "Initial Landing", "title": "Welcome to Unredacted"},
        )


# searching for a document
@require_POST
def search_docs_index(request: HtmxHttpRequest) -> HttpResponse:
    print(request.htmx.trigger)
    global page_info
    context = {"doc_list": [], "title": "", "test": "", "search_query": ""}

    if request.htmx.trigger == "document_search_button":
        search_query = str(request.POST.get("search_query"))

        if search_query is not None:
            url = atlas_url + "/webapp/search/"
            split_query = search_query.split(" ")
            for x in split_query:
                url += f"{x}+"

            url = url[: len(url) - 1]

            response = requests.get(url, headers).json()["data"]

            doc_list = []

            for result in response:
                if result["digitalObjects"] == []:
                    continue

                doc_list.append(Document(raw_json=result))

            context = {
                "doc_list": doc_list,
                "title": f"Search results for {search_query}",
                "test": "document search results",
                "search_query": search_query,
            }

    return render(request, "search_results.html", context)


@require_GET
def display_doc_index(request: HtmxHttpRequest, naId: int) -> HttpResponse:
    print(request.htmx.trigger)

    document = load_doc(naId)

    return render(
        request,
        "document_page.html",
        {
            "test": f"Document load: naId = {naId}",
            "title": document.title,
            "document": document,
        },
    )


@require_GET
def show_pdf(request: HtmxHttpRequest, url: str) -> HttpResponse:
    pdf_content = requests.get(url, headers).content
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="document.pdf"'
    return response


@require_GET
def download_pdf(request: HtmxHttpRequest, url: str) -> HttpResponse:
    pdf_content = requests.get(url, headers).content
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="document.pdf"'
    return response
