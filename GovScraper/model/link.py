from datetime import datetime
from peewee import (
    SqliteDatabase,
    Model,
    AutoField,
    IntegerField,
    TextField,
    CharField,
    FloatField,
    DateTimeField,
)

db = SqliteDatabase("links.db")


class BaseModel(Model):
    class Meta:
        database = db


class LinkModel(BaseModel):
    id = AutoField(unique=True)
    link = TextField(unique=True)
    datetime = DateTimeField(default=datetime.now())

def ReturnLinks():
    db.connect()
    cursor = db.execute_sql('SELECT link FROM linkmodel')
    links=[]
    for row in cursor.fetchall():
        links.append(row[0])
    db.close()
    return links

def ReturnLastLink():
    db.connect()
    cursor = db.execute_sql('SELECT link, datetime FROM linkmodel ')
    res=cursor.fetchone()
    db.close()
    return res[0]

def DeleteLinks(count):
    db.connect()
    qry=LinkModel.delete().limit(count)
    qry.execute()
    db.close()

def AddLinks(link):
    db.connect()
    #qry=LinkModel.delete().limit(count)
    #qry.execute()
    db.close()

def initialize_db():
    db.connect()
    db.create_tables([LinkModel], safe=True)
    db.close()

if __name__ == '__main__':
    #initialize_db()
    pass