from django.apps import AppConfig


class CaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'case'
    verbose_name = 'پرونده های مهاجرتی'

    def ready(self):
        import case.signals
