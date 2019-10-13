from django.contrib import admin
from .models import Country, City, Place, PlaceType, PlaceService


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


@admin.register(PlaceService)
class PlaceServiceAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )


