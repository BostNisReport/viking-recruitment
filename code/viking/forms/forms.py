from django import forms
from django.conf import settings
from django.forms.extras.widgets import SelectDateWidget


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=100, required=False)
    message = forms.CharField(widget=forms.widgets.Textarea)

    error_css_class = 'error'
    required_css_class = 'required'


YES_NO_RADIO = forms.widgets.RadioSelect(choices=(
    (True, 'Yes'),
    (False, 'No'),
))

class CadetApplicationForm(forms.Form):
    academic_requirements = forms.BooleanField(label="Do you meet the 'Minimum Academic Entry Requirements'?", required=False, help_text="""
        <p>A Minimum of 120 UCAS or 48 tariff points, with at least one numerate subject,
        <strong>plus</strong> GCSE grade 'C', level 4 or above in the following subjects:</p>

        <ul>
            <li>Mathematics (grade B, level 6 or above)</li>
            <li>English</li>
            <li>Science (with Physical Science content)</li>
        </ul>
        """, widget=YES_NO_RADIO)
    medical_requirements = forms.BooleanField(label="Do you meet the medical examinations standards?", required=False, help_text="""
        <p>ENG1 for UK and ENG11 for Ireland</p>
        """, widget=YES_NO_RADIO)
    eea_citizen = forms.BooleanField(label="Are you an EEA citizen and have been living in the UK for twelve months prior to starting training?", required=False, widget=YES_NO_RADIO)

    error_css_class = 'error'
    required_css_class = 'required'

    def clean(self):
        cleaned_data = super(CadetApplicationForm, self).clean()

        if (not cleaned_data.get('academic_requirements')
            or not cleaned_data.get('medical_requirements')
            or not cleaned_data.get('eea_citizen')):
            raise forms.ValidationError('We are sorry to advise that you do not meet the critera set by Viking Recruitment at this time.')

        return cleaned_data


class RequestQuoteForm(forms.Form):
    CLASS_LIST = ('Economy', 'Premium Economy / Economy Plus', 'Business', 'First')
    CLASS_CHOICES = [('', '---')] + [(x, x) for x in CLASS_LIST]

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=100)
    number_of_people_travelling = forms.CharField(max_length=100)
    childrens_dates_of_birth = forms.CharField(widget=forms.widgets.Textarea, label='If travelling with children (under 12yrs), please enter their dates of birth:', required=False)
    infant_dates_of_birth = forms.CharField(widget=forms.widgets.Textarea, label='If travelling with infants (up to 2yrs), please enter their dates of birth:', required=False)
    company_vessel_name = forms.CharField(label='Name of vessel/company', max_length=100)
    date_of_flight = forms.DateField(widget=SelectDateWidget, input_formats=settings.DATETIME_INPUT_FORMATS)
    return_date = forms.DateField(widget=SelectDateWidget, input_formats=settings.DATETIME_INPUT_FORMATS)
    preferred_time_of_flight = forms.CharField(max_length=100)
    are_your_dates_flexible = forms.BooleanField(required=False, widget=YES_NO_RADIO)
    departure_location = forms.CharField(label='Departure city/airport', max_length=100)
    arrival_location = forms.CharField(label='Arrival city/airport', max_length=100)
    preferred_class_of_travel = forms.ChoiceField(choices=CLASS_CHOICES)
    preferred_airline = forms.CharField(required=False, max_length=100)
    airline_loyalty_number = forms.CharField(required=False, max_length=100)
    additional_information = forms.CharField(required=False, widget=forms.widgets.Textarea)

    error_css_class = 'error'
    required_css_class = 'required'
