from collections import Counter
from operator import countOf
import classla
import re
from peewee import *
from playhouse.reflection import Introspector


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


class Entities(BaseModel):
    id = PrimaryKeyField()
    entity_name = TextField(default='')
    TotalOccurs = IntegerField(default=0)
    MaxOccursinDoc = IntegerField(default=0)
    OccursInDocs = IntegerField(default=0)


class EntitiesInArticle(BaseModel):
    id_article = ForeignKeyField(Articles, to_field="id", default=0)
    id = ForeignKeyField(Entities, to_field="id", default=0)
    entity_name = TextField(default='')
    occurences = IntegerField(default=0)


Entities.insert(entity_name='PHD', TotalOccurs=0, MaxOccursinDoc=0, OccursInDocs=0).execute()


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
            EntitiesInArticle.insert(id_article=art, id=Entities.select().where(Entities.entity_name == 'Placeholder'),
                                     entity_name=x,
                                     occurences=OccursInDoc).execute()


def updateEntities():
    for art in Articles.select():
        conv = art.body
        conv.strip()
        conv = nlp(conv)
        Words = []
        for x in conv.entities:
            Words.append(x.text)
        Words.sort()
        Words = dupeClear(Words)
        max = 0
        for i in EntitiesInArticle.occurences:
            if max == 0 or i > max:
                max = i
        TotalOccurs = 0
        OccursInDocs = 0
        for x in Words:
            for i in EntitiesInArticle.select().where(EntitiesInArticle.entity_name == x):
                TotalOccurs += i.occurences
            for i in EntitiesInArticle.select().where(EntitiesInArticle.entity_name == x):
                OccursInDocs += 1
            Entities.insert(entity_name=x, TotalOccurs=TotalOccurs, MaxOccursinDoc=max,
                            OccursInDocs=OccursInDocs).execute()
        for i in EntitiesInArticle.select().where(EntitiesInArticle.entity_name == x):
            entity = Entities.get(Entities.entity_name == x)
            i.update(id=entity)


def startDB():
    db.connect()
    Entities.delete()
    EntitiesInArticle.delete()
    db.create_tables([Articles, Entities, EntitiesInArticle], safe=True)
    updateInArts()
    updateEntities()


if __name__ == '__main__':
    db.close()
    startDB()
    cursor = db.execute_sql('select * from entitiesinarticle;')
    for row in cursor.fetchall():
        print(row)
    db.close()