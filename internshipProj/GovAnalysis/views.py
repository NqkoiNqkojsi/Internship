from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from GovAnalysis.models import Articles, EntitiesInArticle
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
    conn = sqliteConnection = sqlite3.connect('../articles.db')
    try:
        cursor = conn.cursor()
        cursor.execute("select * from articlemodel where id="+str(id))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            context=dict({"imgUrl":row[3], "titleCont":row[5], "bodyCont":row[6]})
    finally:
        conn.close()
    return render(request, 'article.html', context)


def ListArticle(request, page):
    conn = sqliteConnection = sqlite3.connect('../articles.db')
    try:
        cursor = conn.cursor()
        cursor.execute("select id, title, date from articlemodel")
        rows = cursor.fetchall()
    finally:
        conn.close()
    
    art_lenght=len(rows)
    paginator = Paginator(SortArticles(rows), 10) # Show 25 contacts per page.
    page_number = page
    page_obj = paginator.get_page(page_number)
    numb4=page+4
    if art_lenght==numb4:
        numb4=-1
    context=dict({"art":page_obj,
     "numb0":page, "numb1":page+1, "numb2":page+2, "numb3":page+3, "numb4":numb4})
    return render(request, 'articlesList.html', context)


def SortArticles(rows):
    return rows.sort(key=lambda x: time.mktime(time.strptime(x[2],"%d.%m.%Y")))

