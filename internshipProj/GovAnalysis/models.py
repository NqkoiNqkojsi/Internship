from django.db import models


class ArtDbManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        # if `use_db` is set on model use that for choosing the DB
        if hasattr(self.model, 'articles'):
            qs = qs.using(self.model.articles)
        #print(qs)
        return qs

class EntDbManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        # if `use_db` is set on model use that for choosing the DB
        if hasattr(self.model, 'entities'):
            qs = qs.using(self.model.entities)
        #print(qs)
        return qs

class EntInArtDbManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.model, 'entitiesInArticle'):
            qs = qs.using(self.model.entitiesInArticle)
        #print(qs)
        return qs

class ArtDbBase(models.Model):
    use_db = 'articles.db'
    objects = ArtDbManager()
    class Meta:
        abstract = True

class EntDbBase(models.Model):
    use_db = 'entities.db'
    objects = EntDbManager()
    class Meta:
        abstract = True

class EntInArtDbBase(models.Model):
    use_db = 'entitiesInArticle.db'
    objects = EntInArtDbManager()
    class Meta:
        abstract = True

# Create your models here.
class Articles(ArtDbBase):
    id=models.AutoField(primary_key=True)
    date = models.TextField()
    url = models.TextField(unique=True)
    images = models.TextField()
    videos = models.TextField()
    title = models.TextField()
    body = models.TextField()
    class Meta:
        managed = False
        db_table = 'articles'
    def _str_(self):
        return self.title

class Entities(EntDbBase):
    id=models.AutoField(primary_key=True)
    entity_name = models.TextField(unique=True)
    TotalOccurs = models.IntegerField()
    MaxOccursinDoc = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'entities'
    def _str_(self):
        return self.entity_name

class EntitiesInArticle(EntInArtDbBase):
    id=models.AutoField(primary_key=True)
    id_article = models.IntegerField()
    id_entity = models.IntegerField()
    entity_name=models.TextField(unique=False)
    occurences = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'entitiesinarticle'
    def _str_(self):
        return self.entity_name