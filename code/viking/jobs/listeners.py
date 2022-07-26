from django.db.models.signals import post_delete, post_save
from .models import Job, JobCandidate


def update_successful_candidates(instance):
    try:
        job = instance.job
        job.successful_candidates = job.jobcandidate_set.filter(stage=4).count()
        job.save(update_fields=['successful_candidates'])
    except Job.DoesNotExist:
        pass


def candidate_postdelete(instance, **kwargs):
    update_successful_candidates(instance)


def candidate_postsave(instance, raw, **kwargs):
    # Don't do anything on import
    if not raw:
        update_successful_candidates(instance)


post_delete.connect(candidate_postdelete, sender=JobCandidate)
post_save.connect(candidate_postsave, sender=JobCandidate)
