from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_.forms import MainUserChangeForm, MainUserCreationForm
from auth_.models import MainUser, Activation


@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    form = MainUserChangeForm
    add_form = MainUserCreationForm

    list_display = ('id', 'email', 'full_name')
    fieldsets = (
        ('Main Fields', dict(fields=(
            'email',
            'full_name',
            'avatar',
        ))),
        ('Password', {'fields': ('password',)}),
        ('Permissions',
         {'fields': ('is_active', 'is_admin', 'is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    ordering = ['email']
    search_fields = ['email']


@admin.register(Activation)
class ActivationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'created_at')
    fields = ('email', 'password', 'is_active')
