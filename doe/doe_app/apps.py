from django.apps import AppConfig
from django.contrib.staticfiles import storage

class DoeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doe_app'

class MyStaticFilesStorage(storage.StaticFilesStorage):
    def __init__(self, *args, **kwargs):
        kwargs['file_permissions_mode'] = 0o640
        kwargs['directory_permissions_mode'] = 0o760
        super().__init__(*args, **kwargs)
