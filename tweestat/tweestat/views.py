from django.http import HttpResponse
from django.shortcuts import redirect, render


def index(request):
    return redirect("/stats/")

def about(request):
    return render(request, 'tweestat/about.html')

def faq(request):
    return render(request, 'tweestat/faq.html')