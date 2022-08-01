from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework import viewsets, generics
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import EntitiesSerializer, EntitiesInArticleSerializer, ArticlesSerializer
from GovAnalysis.models import Articles, EntitiesInArticle, Entities
from django.template import Context, Template
from django.core.paginator import Paginator
from datetime import datetime
import time
import sqlite3


# Create your views here.
def index(request):
    return render(request, 'index.html')

def articlesList(request):
    return render(request, 'articlesList.html')

def entitiesOverv(request):
    return render(request, 'entitiesOverv.html')

def Article(request, id):
    
    try:
        row=Articles.objects.get(id=id)
        context=dict({"imgUrl":row.images, "titleCont":row.title, "bodyCont":row.body, "TopEnt":None})
    finally:
        pass
    conn = sqliteConnection = sqlite3.connect('entitiesInArticles.db')    
    TopEnt=[]
    BotEnt=[]
    try:
        rowsEnt=list(EntitiesInArticle.objects.filter(id_article=id))
        rowsEnt=SortTopInArticle(rowsEnt)
        for rowent in rowsEnt:
            TopEnt.append([str(rowent.id_entity), rowent.entity_name, rowent.occurences])
        context["TopEnt"]=TopEnt
    finally:
        conn.close()
    return render(request, 'article.html', context)


def ListArticle(request, page):
    conn = sqliteConnection = sqlite3.connect('articles.db')
    try:
        cursor = conn.cursor()
        cursor.execute("select id, title, date from articles")
        rows = cursor.fetchall()
    finally:
        conn.close()
    rows=SortAricles(rows)
    art_lenght=len(rows)
    paginator = Paginator(rows, 10) # Show 25 contacts per page.
    page_number = page
    page_obj = paginator.get_page(page_number)
    numb4=page+4
    if art_lenght==numb4:
        numb4=-1
    if page==1:
        context=dict({"art":page_obj,
        "numb0":page, "numb1":page+1, "numb2":page+2, "numb3":page+3, "numb4":numb4})
    else:
        context=dict({"art":page_obj,
        "numb0":page-1, "numb1":page, "numb2":page+1, "numb3":page+2, "numb4":numb4-1})
    return render(request, 'articlesList.html', context)


def EntityOverview(request, id):
    TopEnt=[]
    BotEnt=[]
    try:
        rowEnt=Entities.objects.get(id=id)
        context=dict({"word":rowEnt.entity_name, "len":rowEnt.id, "TotOcc":rowEnt.TotalOccurs, "MaxOcc":rowEnt.MaxOccursinDoc})
    finally:
        pass
    EntArt=[]
    try:
        rowsEntArt=list(EntitiesInArticle.objects.filter(id_entity=rowEnt.id))
        rowsEntArt=SortEntitiesInArticle(rowsEntArt)
        for rowent in rowsEntArt:
            rowArt=Articles.objects.get(id=rowent.id_article)
            EntArt.append([str(rowArt.id), rowArt.title, str(rowent.occurences)])
        context["len"]=len(rowsEntArt)
        context["EntArt"]=EntArt
    finally:
        pass

    return render(request, 'entitiesOverv.html', context)


class EntityViewAPI(viewsets.ModelViewSet):
    print("entity request")
    serializer_class = EntitiesSerializer
    queryset = Entities.objects.all()

class EntitiesInArticleViewAPI(viewsets.ModelViewSet):
    print("entityArticle request")
    serializer_class = EntitiesInArticleSerializer
    queryset = EntitiesInArticle.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_article', 'id_entity']

class ArticlesViewAPI(viewsets.ModelViewSet):
    print("Article request")
    serializer_class = ArticlesSerializer
    queryset = Articles.objects.all()
    filter_backends = [DjangoFilterBackend]


def SortAricles(listArt):
    listArt.sort(key=lambda x: time.mktime(time.strptime(x[2],"%d.%m.%Y")))
    return list(reversed(listArt))

def SortEntitiesInArticle(listEnt):
    listEnt.sort(key=lambda x: x.occurences)
    return list(reversed(listEnt))

def SortTopInArticle(listEnt):
    listEnt.sort(key=lambda x: x.occurences)
    return list(reversed(listEnt))