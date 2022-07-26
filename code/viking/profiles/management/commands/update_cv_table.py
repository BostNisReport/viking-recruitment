# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from viking.auth.models import VikingUser
from viking.profiles.models import CurriculumVitae


class Command(BaseCommand):
    help = "Pre-populate CV model from Document model."

    def update_cv(self, user, document):
        if not CurriculumVitae.objects.filter(user=user).exists():
            cv = CurriculumVitae()
            cv.user = user
            cv.file = document.file
            cv.save()

    def handle(self, *args, **options):
        for user in VikingUser.objects.iterator():
            if user.document_set.count() == 1:
                document = user.document_set.all()[0]
                self.update_cv(user, document)
                document.delete()
            elif user.document_set.count() > 1:
                for document in user.document_set.all():
                    if 'cv' in document.file.name.lower():
                        self.update_cv(user, document)
                        document.delete()

