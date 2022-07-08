from collections import Counter
from operator import countOf

from django.forms import IntegerField
import classla
import re
from peewee import (
    SqliteDatabase,
    Model,
    AutoField,
    IntegerField,
    TextField,
    CharField,
    FloatField,
    DateTimeField
)
from playhouse.reflection import Introspector
from datetime import datetime

db = SqliteDatabase('articles.db')

class BaseModel(Model):
    class Meta:
        database = db

class ArticleModel(BaseModel):
    id = AutoField(unique=True)
    date = DateTimeField(default=datetime.now())
    url = TextField(unique=True)
    images = TextField()
    videos = TextField()
    title = TextField()
    body = TextField()

class Entities(BaseModel):
    id = AutoField(unique=True)
    entity_name = TextField(default='')
    TotalOccurs = IntegerField(default=0)
    MaxOccursinDoc = IntegerField(default=0)


class EntitiesInArticle(BaseModel):
    id = AutoField(unique=True)
    id_article = IntegerField()
    id_entity = IntegerField()
    entity_name = TextField(default='')
    occurences = IntegerField(default=0)


def CheckWord(word):
    query = Entities.select().where(Entities.entity_name == word)
    for res in query:
        print(res.TotalOccurs)
    


if __name__ == '__main__':
    db.close()
    db.connect()
    CheckWord("Бойко Борисов")
    db.close()