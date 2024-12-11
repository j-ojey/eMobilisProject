from django.apps import AppConfig

''' To make Django recognize signals.py file, you need to import it in your app's apps.py. '''
class appConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals
