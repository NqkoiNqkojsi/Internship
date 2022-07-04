import datetime
from playhouse.reflection import generate_models, print_model, Introspector
import classla
from collections import Counter
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


# Gets the meat of the articles from the db
def getLinks():
    try:
        db.close()
    except:
        pass
    db.connect()
    cursor = db.execute_sql('SELECT body FROM articlemodel')
    links = []
    for row in cursor.fetchall():
        links.append(row[0])
    db.close()
    return links


# DB setup
db = SqliteDatabase('articles.db', pragmas={'journal_mode': 'wal'})
introspector = Introspector.from_database(db)
allBodies = getLinks()
NLPWords = []
NLPTotalOccurs = 0
NLPOccursinDocs = 0

# Setting up the NLP

classla.download('bg')
nlp = classla.Pipeline('bg', processors='ner, tokenize')

articles_src = introspector.generate_models()
Articles = articles_src['articlemodel']


class BaseModel(Model):
    class Meta:
        database = db


class Entities(BaseModel):
    id_entity = AutoField()
    entity_name = TextField(unique=True)
    TotalOccurs = IntegerField()
    TotalOccursinDoc = IntegerField()
    OccursInDocs = IntegerField()



class EntitiesInArticle(BaseModel):
    id_article = ForeignKeyField(Articles, to_field="id", related_name="ArticleIDs")
    id_entity = ForeignKeyField(Entities, to_field="id_entity", related_name="EntityIDs")
    occurences = IntegerField()

# def updateEntities():
#     for i in allBodies:
#         conv = nlp(i)
#         NLPWords.clear()
#         for x in conv.entities:
#             NLPWords.append(x.text)
#             NLPWords.sort()
#             NLPTotalOccurs += NLP




def startDB():
    db.connect()
    db.create_tables([Articles, Entities, EntitiesInArticle], safe=True)
    db.close()


if __name__ == '__main__':
    startDB()
