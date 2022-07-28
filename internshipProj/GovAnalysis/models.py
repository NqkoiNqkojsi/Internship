from django.db import models

# Create your models here.
class Articles(models.Model):
    date = models.DateTimeField()
    url = models.TextField(unique=True)
    images = models.TextField()
    videos = models.TextField()
    title = models.TextField()
    body = models.TextField()

    def _str_(self):
        return self.title

class Entities(models.Model):
    entity_name = models.TextField(unique=True)
    TotalOccurs = models.IntegerField()
    TotalOccursinDoc = models.IntegerField()

    def _str_(self):
        return self.entity_name

class EntitiesInArticle(models.Model):
    id_article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    id_entity = models.ForeignKey(Entities, on_delete=models.CASCADE)
    entity_name=models.TextField(unique=False)
    occurences = models.IntegerField()

    def _str_(self):
        return self.entity_name