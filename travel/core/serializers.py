from rest_framework import serializers
from .models import Place, PlaceUserRating


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


class PlaceUserRatingSerialzier(serializers.ModelSerializer):
    class Meta:
        model = PlaceUserRating
        fields = '__all__'


class AddRatingSerializer(serializers.Serializer):

    def add_rating(self, place, user):
        data = self.context['request'].data
        rating = PlaceUserRating.objects.add_rating(place=place, user=user, review=data['review'], rating=data['rating'])
        return {'rating': PlaceUserRatingSerialzier(rating).data}