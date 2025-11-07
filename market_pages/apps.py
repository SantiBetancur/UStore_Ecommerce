from django.apps import AppConfig
from django.utils.module_loading import import_string
from django.conf import settings 

class MarketPagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market_pages'
    def ready(self):
        self.image_storage_class = import_string(settings.IMAGE_STORAGE_CLASS)