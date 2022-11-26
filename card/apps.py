from django.apps import AppConfig


class CardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'card'

    def ready(self) -> None:
        import card.signals
        return super().ready()