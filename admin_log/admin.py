from django.contrib import admin
from .models import CustomLogEntry


@admin.register(CustomLogEntry)
class CustomLogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr',  'action_flag']
