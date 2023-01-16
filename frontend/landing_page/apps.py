from django.apps import AppConfig


class LandingPageConfig(AppConfig):
    """Config for LandingPage app.

    Args:
        AppConfig (AppConfig): AppConfig
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landing_page'
