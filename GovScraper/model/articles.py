from datetime import datetime
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

db = SqliteDatabase("internshipProj/articles.db")


class BaseModel(Model):
    class Meta:
        database = db


class Articles(BaseModel):
    id = AutoField(unique=True)
    date = DateTimeField(default=datetime.now())
    url = TextField(unique=True)
    images = TextField()
    videos = TextField()
    title = TextField()
    body = TextField()

def ReturnArticles():
    try:
        db.connect()
    except:
        pass
    cursor = db.execute_sql('SELECT body FROM article')
    bodies=[]
    for row in cursor.fetchall():
        bodies.append(row[0])
    db.close()
    return bodies

def DeleteArticles():
    try:
        db.connect()
    except:
        pass
    query=Articles.delete().where(Articles.id>5)
    query.execute()
    db.close()


def initialize_db():
    db.connect()
    db.create_tables([Articles], safe=True)
    db.close()

if __name__ == '__main__':
    #initialize_db()
    DeleteArticles()
