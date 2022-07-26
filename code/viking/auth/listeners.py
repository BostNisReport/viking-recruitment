from django.db.models.signals import post_delete, post_save
from viking.profiles.models import PreviousWork
from .models import VikingUser


def update_latest_position(instance):
    try:
        # Get the user fresh
        user = VikingUser.objects.get(id=instance.user_id)
        try:
            new_latest_position = user.previouswork_set.all()[0]
        except IndexError:
            new_latest_position = None

        # Only update if needed
        if user.latest_position != new_latest_position:
            user.latest_position = new_latest_position
            user.save(update_fields=['latest_position'])
    except VikingUser.DoesNotExist:
        pass


def previouswork_postdelete(instance, **kwargs):
    update_latest_position(instance)


def previouswork_postsave(instance, raw, **kwargs):
    # Don't do anything on import
    if not raw:
        update_latest_position(instance)


post_delete.connect(previouswork_postdelete, sender=PreviousWork)
post_save.connect(previouswork_postsave, sender=PreviousWork)
