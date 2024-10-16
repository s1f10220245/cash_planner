from django.apps import AppConfig


class CashPlannerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cash_planner'

    def ready(self):
        import cash_planner.signals
