from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        depth = 2


class PlaceSearchSerializer(serializers.Serializer):

    def search(self, query):
        from django.contrib.postgres.search import TrigramSimilarity
        from utils import constants
        kwargs = {}
        kwargs['similarity__gt'] = constants.SEARCH_SIMILARITY
        places = []
        for place in Place.objects.annotate(similarity=TrigramSimilarity('name', query), ).filter(**kwargs):
            places.append(place)
        return {'places': PlaceSerializer(places, many=True).data}
