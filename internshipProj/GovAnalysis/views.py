from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from GovAnalysis.models import Articles, EntitiesInArticle
from django.template import Context, Template
import sqlite3


# Create your views here.
def index(request):
    return render(request, 'header.html')


def article(request, id):
    row = Articles.objects.all()
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


