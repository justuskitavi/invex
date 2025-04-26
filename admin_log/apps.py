from django.apps import AppConfig

class AdminLogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_log'

    def ready(self):
        from django.contrib.admin.models import LogEntry
        from django.contrib.admin.options import ModelAdmin
        from django.contrib.admin.sites import AdminSite
        from .models import CustomLogEntry

        #Monkey patch the admin tom use CustomLogEntry
        import django.contrib.admin.models as admin_models
        admin_models.LogEntry = CustomLogEntry
