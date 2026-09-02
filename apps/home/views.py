from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
def home(req: HttpRequest) -> HttpResponse:
    return render(
        req,
        "home/home.html",
    )
