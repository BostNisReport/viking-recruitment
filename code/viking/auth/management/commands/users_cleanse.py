# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from blanc_pages.models.pages import PageVersion
from dateutil.relativedelta import relativedelta

from viking.auth.models import VikingUser


class Command(BaseCommand):
    help = 'Clean profiles'

    def handle(self, *args, **options):
        now = timezone.now()

        # Make sure we don't delete any pages.
        owners_ids = PageVersion.objects.order_by().values_list('owner__id', flat=True).distinct()

        five_years_ago = now - relativedelta(years=5)
        month_ago = now - relativedelta(months=1)

        base_list = VikingUser.objects.exclude(
            Q(id__in=owners_ids) |
            Q(date_joined__gte=month_ago) |
            Q(is_superuser=True) |
            Q(is_staff=True)
        )
        filters = [
            # Hasn't updated for 5 years and no recruiter notes.
            {'updated__lte': five_years_ago, 'recruiternote__date__lte': five_years_ago},

            # Don't have CV and no recruiter notes.
            {'curriculumvitae__isnull': True, 'recruiternote__isnull': True},

            # Remove inactive users.
            {'is_staff': False, 'is_active': False},
            {'email__icontains': 'whitehall-dress'},
            {'email__iregex': r'(.*\.){6,100}'},
            {'email__icontains': 'email7d4'},
            {'email__icontains': 'SergoWefCQ'},
            {'first_name': 'petyunchik-JoichUK'},
            {'first_name': 'AnetLopezKiOA'},
            {'first_name': 'DenWefCA'},
            {'first_name': 'FlalordiliKR'},
            {'first_name': 'gelsRonienemiAP'},
            {'first_name': 'OvereGorkAP'},
            {'first_name': 'DouglastowBN'},
            {'first_name': 'DeniseEtAC'},
            {'first_name': 'JessicateaxKW'},
            {'first_name': 'MarilynbabAP'},
        ]

        for query_filter in filters:
            for obj in base_list.filter(**query_filter).iterator():
                obj.delete()
