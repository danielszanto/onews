from django.apps import AppConfig
from django.conf import settings


class NewsConfig(AppConfig):
    name = 'news'
    def ready(self):
        from scheduler import scheduler
        if settings.SCHEDULER_AUTOSTART: #turn off when using pytest
            scheduler.start()    
