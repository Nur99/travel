from django.contrib import admin
from .models import (Event, Order, Ticket, Test)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'place', 'price', 'timestamp')
    search_fields = ('name', )
    list_filter = ('place', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'quantity', 'status')
    list_filter = ('event', 'event__place', 'status')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('order', 'uuid', )
    list_filter = ('order', )


admin.site.register(Test)