from django.contrib import admin

from .models import Habitica


class HabiticaAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Wunderlist',
            {'fields': ['user_id', 'name', 'email', 'api_token', 'owner', 'created_at', 'modified_at']}
        )
    ]
    readonly_fields = ['created_at', 'modified_at']
    list_display = ['user_id', 'name', 'email', 'owner', 'created_at', 'modified_at']


admin.site.register(Habitica, HabiticaAdmin)
