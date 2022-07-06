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


# Most frequent word per list
def most_frequent(list):
    counter = 0
    word = list[0]

    for i in list:
        curr_frequency = list.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            word = i

    return word


# Ranks all the named entities in the list based on amount
def RankingPerDoc(list):
    counts = dict(Counter(list))
    for i in counts:
        print(i, list[i])


def dupeClear(list1):
    return list(dict.fromkeys(list1))


# Top 3 most seen words per list
def top3_ranking(l):
    l.sort()
    top3 = []
    for i in range(3):
        top3.append(most_frequent(l))
        l = list(filter(lambda x: x != most_frequent(l), l))
    return top3


# DB setup
db = SqliteDatabase('articles.db', pragmas={'journal_mode': 'wal'})
introspector = Introspector.from_database(db)
NLPWords = []

# Setting up the NLP

classla.download('bg')
nlp = classla.Pipeline('bg', processors='ner, tokenize')

articles_src = introspector.generate_models()
Articles = articles_src['articlemodel']


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




def updateInArts():
    for art in Articles:
        conv = art.body
        conv.strip()
        conv = nlp(conv)
        NLPWords.clear()
        for x in conv.entities:
            NLPWords.append(x.text)
        NLPWords.sort()
        OccursInDoc = 0
        for x in NLPWords:
            OccursInDoc = countOf(NLPWords, x)
        NLPWords2 = dupeClear(NLPWords)
        for x in NLPWords2:
            query = Entities.get_or_none(Entities.entity_name == x)
            if query is not None:
                EntitiesInArticle.create(id_article=art, id_entity=query.id,
                                        entity_name=x,
                                        occurences=OccursInDoc)
                updateEntities(x, OccursInDoc)
            else:
                createEntity(x, OccursInDoc)


def createEntity(x, occ):
    print("Making:"+str(x))
    Entities.create(entity_name=x, TotalOccurs=occ, MaxOccursinDoc=occ)

def updateEntities(x, occ):
    print("Updating:"+str(x))
    tot=Entities.get(Entities.entity_name==x).TotalOccurs
    occ=occ+tot
    Entities.update(TotalOccurs=occ).where(Entities.entity_name==x)
    most=Entities.get(Entities.entity_name==x).MaxOccursinDoc
    if occ>most:
        Entities.update(MaxOccursinDoc=occ).where(Entities.entity_name==x)



def startDB():
    db.connect()
    Entities.delete()
    EntitiesInArticle.delete()
    db.create_tables([Articles, Entities, EntitiesInArticle], safe=True)
    updateInArts()


if __name__ == '__main__':
    db.close()
    startDB()
    cursor = db.execute_sql('select * from entitiesinarticle')
    for row in cursor.fetchall():
        print(row)
    db.close()