# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils import timezone

from viking.profiles.models import PreviousWork
from viking.profiles.choices import CONTACT_EMPLOYER_CHOICES


class Command(BaseCommand):
    help = "Update previous work fields with dummy information to prevent formsets to fail."

    def handle(self, *args, **options):
        counter = 0
        for previous_work in PreviousWork.objects.iterator():
            changed = False

            if not previous_work.employer_name:
                changed = True
                previous_work.employer_name = BLANK_CHOICE_DASH[0][1]

            if not previous_work.permission_to_make_contact:
                # Set as 'N'
                changed = True
                previous_work.permission_to_make_contact = CONTACT_EMPLOYER_CHOICES[1][0]

            if not previous_work.reason_for_leaving:
                changed = True
                previous_work.reason_for_leaving = BLANK_CHOICE_DASH[0][1]

            if not previous_work.date_available_for_employment:
                changed = True
                previous_work.date_available_for_employment = timezone.now()

            if changed:
                counter += 1
                previous_work.save()
                print counter
