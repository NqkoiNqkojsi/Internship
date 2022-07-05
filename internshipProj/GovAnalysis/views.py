from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from GovAnalysis.models import Articles, EntitiesInArticle
from django.template import Context, Template
from django.core.paginator import Paginator
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
    
    paginator = Paginator(rows, 20) # Show 25 contacts per page.
    page_number = page
    page_obj = paginator.get_page(page_number)
    return render(request, 'articlesList.html')


