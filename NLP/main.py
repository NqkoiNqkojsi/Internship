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
#db = SqliteDatabase('articles.db', pragmas={'journal_mode': 'wal'})
dbArt = SqliteDatabase('articles.db')
dbEnt = SqliteDatabase('entities.db')
dbEntInArt = SqliteDatabase('entitiesInArticles.db')
introspectorArt = Introspector.from_database(dbArt)
NLPWords = []

# Setting up the NLP

classla.download('bg')
nlp = classla.Pipeline('bg', processors='ner, tokenize')

articles_src = introspectorArt.generate_models()
Articles = articles_src['articlemodel']


class ArtModel(Model):
    class Meta:
        database = dbArt

class EntModel(Model):
    class Meta:
        database = dbEnt

class EntInArtModel(Model):
    class Meta:
        database = dbEntInArt

class ArticleModel(ArtModel):
    id = AutoField(unique=True)
    date = DateTimeField(default=datetime.now())
    url = TextField(unique=True)
    images = TextField()
    videos = TextField()
    title = TextField()
    body = TextField()

class Entities(EntModel):
    id = AutoField(unique=True)
    entity_name = TextField(default='')
    TotalOccurs = IntegerField(default=0)
    MaxOccursinDoc = IntegerField(default=0)


class EntitiesInArticle(EntInArtModel):
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
        NLPWords=[]
        for x in conv.entities:
            NLPWords.append(x.text)
        NLPWords.sort()
        OccursInDoc = 0
        oldWords=[]
        for word in NLPWords:
            if not word in oldWords:
                OccursInDoc = countOf(NLPWords, word)
                ent = Entities.get_or_none(Entities.entity_name == word)
                if ent is not None:
                    EntitiesInArticle.create(id_article=art, id_entity=ent.id,
                                            entity_name=word,
                                            occurences=OccursInDoc)
                    updateEntities(ent, word, OccursInDoc)
                else:
                    id_ent=createEntity(word, OccursInDoc)
                    EntitiesInArticle.create(id_article=art, id_entity=id_ent,
                                            entity_name=word,
                                            occurences=OccursInDoc)
                oldWords.append(word)
            
            


def createEntity(x, occ):
    print("Making:"+str(x))
    ent=Entities.create(entity_name=x, TotalOccurs=occ, MaxOccursinDoc=occ)
    ent.save()
    return ent.id

def updateEntities(ent, x, occ):
    print("Updating:"+str(x))
    ent.TotalOccurs=occ+ent.TotalOccurs
    if occ>ent.MaxOccursinDoc:
        ent.MaxOccursinDoc=occ
    print(ent.save())



def startDB():
    dbArt.connect()
    dbEnt.connect()
    dbEntInArt.connect()
    Entities.delete()
    EntitiesInArticle.delete()
    dbArt.create_tables([Articles], safe=True)
    dbEnt.create_tables([Entities], safe=True)
    dbEntInArt.create_tables([EntitiesInArticle], safe=True)
    updateInArts()


if __name__ == '__main__':
    dbArt.close()
    dbEnt.close()
    dbEntInArt.close()
    startDB()
    dbArt.close()
    dbEnt.close()
    dbEntInArt.close()