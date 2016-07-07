from django.contrib import admin

from .models import Wunderlist, Connection


class WunderlistAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Wunderlist',
            {'fields': ['user_id', 'name', 'email', 'api_token', 'owner', 'created_at', 'modified_at']}
        )
    ]
    readonly_fields = ['created_at', 'modified_at']
    list_display = ['user_id', 'name', 'email', 'owner', 'created_at', 'modified_at']


class ConnectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Connection',
            {'fields': ['list_id', 'list_title', 'habit_id', 'habit_title', 'token', 'webhook_id', 'owner']}
        ),
        (
            'Activity',
            {'fields': ['is_active', 'tasks_completed', 'last_upscored', 'created_at', 'modified_at']}
        )
    ]
    readonly_fields = ['list_id', 'list_title', 'token', 'webhook_id', 'created_at', 'modified_at']
    list_display = ['list_id', 'list_title', 'habit_id', 'habit_title', 'token', 'is_active', 'owner', 'tasks_completed', 'created_at', 'modified_at']


admin.site.register(Wunderlist, WunderlistAdmin)
admin.site.register(Connection, ConnectionAdmin)
