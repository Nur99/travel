from django.contrib import admin
from .models import (Country, City, Place, PlaceType, PlaceService,
                    PlaceUserRating)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'rating')
    search_fields = ('name', )
    list_filter = ('city__country', 'city')

    def country(self, obj):
        return obj.city.country
    country.short_description = "Страна заведения"


@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(PlaceService)
class PlaceServiceAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(PlaceUserRating)
class PlaceUserRatingAdmin(admin.ModelAdmin):
    list_display = ('place', 'user', 'rating', 'review', 'status')
    search_fields = ('place__name', )
    list_filter = ('status', )
