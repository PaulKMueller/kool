from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class ResultpageConfig(ModuleMixin, AppConfig):
    """Config for ResultPage app.

    Args:
        ModuleMixin (Any): ModuleMixin
        AppConfig (AppConfig): AppConfig
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "ResultPage"
    icon = '<i class="material-icons">flight_takeoff</i>'
