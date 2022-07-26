from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'viking.profiles'
    label = 'profiles'

    def ready(self):
        super(ProfilesConfig, self).ready()
        from . import listeners  # noqa
