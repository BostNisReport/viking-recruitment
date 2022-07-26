from blanc_pages_form_block.models import BaseFormBlock, BaseFormNoEmailBlock


class ContactFormBlock(BaseFormBlock):
    form_class = 'viking.forms.forms.ContactForm'

    class Meta:
        verbose_name = 'contact form'


class CadetApplicationFormBlock(BaseFormNoEmailBlock):
    form_class = 'viking.forms.forms.CadetApplicationForm'

    class Meta:
        verbose_name = 'cadet application form'


class RequestQuoteFormBlock(BaseFormBlock):
    form_class = 'viking.forms.forms.RequestQuoteForm'

    class Meta:
        verbose_name = 'request quote form'
