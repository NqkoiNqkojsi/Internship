import datetime
from playhouse.reflection import generate_models, print_model, Introspector
import classla
from collections import Counter
from operator import countOf
from peewee import *


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
    entity_name = TextField(default='', unique=True)
    TotalOccurs = IntegerField(default=0)
    MaxOccursinDoc = IntegerField(default=0)
    OccursInDocs = IntegerField(default=0)


class EntitiesInArticle(BaseModel):
    id_article = ForeignKeyField(Articles, to_field="id", default=0)
    id = ForeignKeyField(Entities, to_field="id", default=0)
    entity_name = TextField(default='')
    occurences = IntegerField(default=0)


def updateEntities():
    for art in Articles.select():
        conv = art.body
        conv.strip()
        conv = nlp(conv)
        NLPWords.clear()
        for x in conv.entities:
            NLPWords.append(x.text)
            NLPWords.sort()

        for x in NLPWords:

            OccursInDoc = countOf(NLPWords, x)
            existQuery = Entities.select().where(Entities.entity_name == x)
            if existQuery.exists():
                entity = Entities.get(Entities.entity_name == x)
                entity.OccursInDocs += 1
                entity.TotalOccurs += OccursInDoc
                if entity.MaxOccursinDoc < OccursInDoc:
                    entity.MaxOccursinDoc = OccursInDoc
            else:
                Entities.insert(entity_name=x, TotalOccurs=OccursInDoc, MaxOccursinDoc=OccursInDoc,
                                OccursInDocs=1).execute()


def updateInArts():
    for article in Articles:
        conv = article.body
        conv.strip()
        conv = nlp(conv)
        NLPWords.clear()
        for x in conv.entities:
            NLPWords.append(x.text)
            NLPWords.sort()
        for x in NLPWords:
            OccursInDoc = countOf(NLPWords, x)
            entity = Entities.get(Entities.entity_name == x)
            name = entity.entity_name
            EntitiesInArticle.insert(id_article=article, id=entity, entity_name=name,
                                     occurences=OccursInDoc).execute()


def startDB():
    db.connect()
    db.create_tables([Articles, Entities, EntitiesInArticle], safe=True)
    updateEntities()
    updateInArts()


if __name__ == '__main__':
    db.close()
    startDB()
    cursor = db.execute_sql('select * from entities;')
    for row in cursor.fetchall():
        print(row)
    db.close()