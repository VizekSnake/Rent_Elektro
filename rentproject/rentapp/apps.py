from django.apps import AppConfig


class RentappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rentapp'


class CoreConfig(AppConfig):
    name = 'core'
