from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from GovAnalysis.models import Articles, EntitiesInArticle
from django.template import Context, Template

# Create your views here.
def index(request):
    return render(request, 'header.html')


def article(request, id):
    row = Articles.objects.all()
    return render(request, 'article.html')


