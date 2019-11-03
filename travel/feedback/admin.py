from django.contrib import admin
from .models import (Feedback)


@admin.register(Feedback)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )
    list_filter = ('user', )
