from django.apps import AppConfig


class LibrarywebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'libraryweb'
    def ready(self):
        import libraryweb.signals