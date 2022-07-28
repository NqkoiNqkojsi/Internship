from rest_framework import serializers
from .models import Entities, Articles, EntitiesInArticle

class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = ('id', 'title', 'description', 'completed')