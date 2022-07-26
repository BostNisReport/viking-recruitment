# -*- coding: utf-8 -*-

import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand

from viking.auth.emails import send_prompt_email_to_update_profile
from viking.auth.models import VikingUser


class Command(BaseCommand):
    help = "Prompt client to update their profile."

    def handle(self, *args, **options):

        YEAR = 365
        WEEK = 7
        MONTH = 28

        now = timezone.now()

        # Reduce a query for qs.
        year = now + timezone.timedelta(days=368)
        year_2014 = datetime.datetime(2014, 1, 1)

        for user in VikingUser.objects.filter(
                is_staff=False, date_joined__gte=year_2014, date_joined__lte=year
        ):
            # One year send email to everyone as reminder to update their profile.
            if (now - user.date_joined).days == YEAR:
                self.update_user_prompt_email(user, period='year')

            # Send in one week time.
            elif (now - user.date_joined).days == WEEK:
                self.update_user_prompt_email(user, 'week')

            # Send in three months.
            elif (now - user.date_joined).days == MONTH * 3:
                self.update_user_prompt_email(user, period='three months')

    def update_user_prompt_email(self, user, period):
        """Mark that prompt email is sent and date it was sent."""

        user.prompt_email_sent = True
        user.prompt_email_sent_date = datetime.datetime.now()
        user.save()

        send_prompt_email_to_update_profile(user, period)

