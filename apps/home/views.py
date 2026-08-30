from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
def hello_world(req: HttpRequest) -> HttpResponse:
    return render(
        req,
        "hello_world.html",
    )


def home(req: HttpRequest) -> HttpResponse:
    return render(
        req,
        "home/home.html",
    )
