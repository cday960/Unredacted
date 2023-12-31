from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET

from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# Create your views here.
@require_GET
def index(request: HtmxHttpRequest) -> HttpResponse:
    # this shows the trigger event in the django server terminal
    print(request.htmx.trigger)
    if request.htmx.trigger == "replace_button":
        context = {"test": "Button pressed!"}
        # this entire html file is returned and placed into the target of the call
        return render(request, "components/_partial.html", context)
    else:
        context = {"test": "Initial page load"}
        return render(request, "dashboard/index.html", context)
