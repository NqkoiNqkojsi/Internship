from rest_framework import serializers
from .models import Entities, Articles, EntitiesInArticle

class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = ('id', 'entity_name', 'TotalOccurs', 'MaxOccursinDoc')


class EntitiesInArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntitiesInArticle
        fields = ('id', 'id_article', 'id_entity', 'entity_name', 'occurences')
    
class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('id', 'date', 'url', 'images', 'videos', 'title', 'body')