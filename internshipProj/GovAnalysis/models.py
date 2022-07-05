from django.db import models

# Create your models here.
class Articles(models.model):
    id = models.AutoField(unique=True)
    date = models.DateTimeField()
    url = models.TextField(unique=True)
    images = models.TextField()
    videos = models.TextField()
    title = models.TextField()
    body = models.TextField()

class Entities(models.model):
    id_entity = models.AutoField()
    entity_name = models.TextField(unique=True)
    TotalOccurs = models.IntegerField()
    TotalOccursinDoc = models.IntegerField()
    OccursInDocs = models.IntegerField()

class EntitiesInArticle(models.model):
    id_article = models.ForeignKeyField(Articles, to_field="id", related_name="ArticleIDs")
    id_entity = models.ForeignKeyField(Entities, to_field="id_entity", related_name="EntityIDs")
    occurences = models.IntegerField()