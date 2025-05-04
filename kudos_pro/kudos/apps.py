# kudos/apps.py
from django.apps import AppConfig

class KudosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kudos'

    def ready(self):
        pass  # Remove the signals import for now