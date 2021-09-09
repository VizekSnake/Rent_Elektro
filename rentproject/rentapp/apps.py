from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'rentapp'

    def ready(self):
        import rentapp.signals