from django.db import models

# Create your models here.
class Articles(models.Model):
    date = models.DateTimeField()
    url = models.TextField(unique=True)
    images = models.TextField()
    videos = models.TextField()
    title = models.TextField()
    body = models.TextField()

class Entities(models.Model):
    entity_name = models.TextField(unique=True)
    TotalOccurs = models.IntegerField()
    TotalOccursinDoc = models.IntegerField()
    OccursInDocs = models.IntegerField()

class EntitiesInArticle(models.Model):
    id_article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    id_entity = models.ForeignKey(Entities, on_delete=models.CASCADE)
    occurences = models.IntegerField()