from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'header.html')


def article(request, id):
    return render(request, 'article.html')


