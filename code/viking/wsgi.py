"""
WSGI config for viking project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("VIKINGRECRUITMENT_SETTINGS_MODULE", "viking.settings.production"))

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# New Relic
if os.environ.get('NEW_RELIC_LICENSE_KEY') is not None:
    import newrelic.agent
    newrelic.agent.initialize()
    application = newrelic.agent.WSGIApplicationWrapper(application)
