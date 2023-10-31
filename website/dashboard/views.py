from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET

from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# Create your views here.
@require_GET
def index(request: HtmxHttpRequest) -> HttpResponse:
    return render(request, "dashboard/index.html")
