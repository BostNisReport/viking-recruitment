# -*- coding: utf-8 -*-

from django.db import transaction
from django.core.management.base import BaseCommand

from viking.auth.models import VikingUser
from viking.profiles.models import CompetencyCertificate, Country


class Command(BaseCommand):
    help = "Pre-populate new table for certificates."

    @transaction.commit_on_success
    def handle(self, *args, **options):
        for user in VikingUser.objects.iterator():
            if user.coc_certificate:
                cc = CompetencyCertificate()
                cc.user = user
                cc.certificate = user.coc_certificate
                if user.coc_issuing_authority.code:
                    country = Country.objects.get(iso_3166_1_a2=user.coc_issuing_authority.code)
                else:
                    country = None
                cc.issuing_authority = country
                cc.expiry_date = user.coc_expiry_date
                cc.save()
