from django.apps import AppConfig


class VideoflixbackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videoflixbackend'


    def ready(self):
        import videoflixbackend.signals