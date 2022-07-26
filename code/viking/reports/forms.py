from django import forms
from viking.jobs.models import Job
import datetime


def today_minus_30():
    return datetime.date.today() - datetime.timedelta(days=30)


class ApplicationsReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'datepicker'}), initial=today_minus_30)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'datepicker'}), initial=datetime.date.today)

    def clean(self):
        cleaned_data = super(ApplicationsReportForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("End date is before start date")

        # Always return the full collection of cleaned data.
        return cleaned_data


class JobsReportForm(forms.Form):
    JOB_FILTER_CHOICES = (
        ('', 'All'),
    ) + Job.JOB_STATUS_CHOICES
    JOB_FILTER_DICT = dict(JOB_FILTER_CHOICES)

    job_filter = forms.ChoiceField(choices=JOB_FILTER_CHOICES, required=False)
