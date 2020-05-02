from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'auth_'

    def ready(self):
        import auth_.signals
