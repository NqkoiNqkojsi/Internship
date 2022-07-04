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

db = SqliteDatabase("articles.db")


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


def initialize_db():
    db.connect()
    db.create_tables([ArticleModel], safe=True)
    db.close()

if __name__ == '__main__':
    initialize_db()