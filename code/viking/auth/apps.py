from django.apps import AppConfig


class VikingAuthConfig(AppConfig):
    name = 'viking.auth'
    label = 'viking_auth'
    verbose_name = 'Auth'

    def ready(self):
        super(VikingAuthConfig, self).ready()
        from . import listeners  # noqa
