from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from GovAnalysis.models import Articles, EntitiesInArticle
from django.template import Context, Template
from django.core.paginator import Paginator
from datetime import datetime
import sqlite3


# Create your views here.
def index(request):
    return render(request, 'header.html')


def Article(request, id):
    conn = sqliteConnection = sqlite3.connect('../articles.db')
    try:
        cursor = conn.cursor()
        cursor.execute("select * from articlemodel where id="+str(id))
        rows = cursor.fetchall()
        for row in rows:
            context=dict({"imgUrl":row[3], "titleCont":row[5], "bodyCont":row[6], "TopEnt":None})
    finally:
        pass
    TopEnt=[]
    BotEnt=[]
    try:
        cursor = conn.cursor()
        cursor.execute("select * from entitiesinarticle where id_article="+str(id))
        rowsEnt = cursor.fetchall()
        for rowent in rowsEnt:
            TopEnt.append([str(rowent[2]), rowent[3], rowent[4]])
        context["TopEnt"]=TopEnt
    finally:
        conn.close()
    print(context)
    return render(request, 'article.html', context)


def ListArticle(request, page):
    numb=[page, page+1, page+2, page+3, page+4]
    conn = sqliteConnection = sqlite3.connect('../articles.db')
    try:
        cursor = conn.cursor()
        cursor.execute("select id, title, date from articlemodel")
        rows = cursor.fetchall()
    finally:
        conn.close()
    
    art_lenght=len(rows)
    # TO DO Sort
    paginator = Paginator(rows, 10) # Show 25 contacts per page.
    page_number = page
    page_obj = paginator.get_page(page_number)
    numb4=page+4
    if art_lenght==numb4:
        numb4=-1
    context=dict({"art":page_obj,
     "numb0":page, "numb1":page+1, "numb2":page+2, "numb3":page+3, "numb4":numb4})
    return render(request, 'articlesList.html', context)


def EntityOverview(request, id):
    conn = sqliteConnection = sqlite3.connect('../articles.db')
    TopEnt=[]
    BotEnt=[]
    try:
        cursor = conn.cursor()
        cursor.execute("select * from entities where id="+str(id))
        rows = cursor.fetchall()
        for row in rows:
            context=dict({"id":row[0], "word":row[1], "TotOcc":row[2], "MaxOcc":row[3]})
    finally:
        conn.close()
    
    return render(request, 'entitiesOverv.html', context)

