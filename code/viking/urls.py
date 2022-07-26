# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Additional imports
from blanc_pages import block_admin
from viking.jobsatsea.views import JobsRedirectView, ProfileJobsRedirectView

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    # Blanc pages block admin
    url(r'^blockadmin/', include(block_admin.site.urls)),

    # News
    url(r'^news/', include('viking.news.urls', namespace='blanc_basic_news')),

    # Team
    url(r'^team/', include('viking.team.urls', namespace='team')),

    # Jobs at sea frontend
    url(r'^jobs/', include('viking.jobsatsea.urls', namespace='jobsatsea', app_name='jobsatsea')),

    url(
        r'^profile/jobs/',
        include('viking.jobsatsea.urls', namespace='profiles_jos', app_name='jobsatsea'),
        {
            'base_template': 'jobsatsea/base_profile.html',
        }
    ),
    url(r'^jobsatsea/(?P<jobsatsea_url>.*)', JobsRedirectView.as_view()),
    url(r'^profile/jobsatsea/(?P<jobsatsea_url>.*)', ProfileJobsRedirectView.as_view()),

    # Events
    url(r'^events/', include('blanc_basic_events.events.urls', namespace='blanc_basic_events')),

    # Downloads
    url(r'^downloads/', include('viking.downloads.urls', namespace='downloads')),

    # Accounts/registration
    url(r'^accounts/', include('viking.auth.urls')),

    # User profiles
    url(r'^profile/', include('viking.profiles.urls', namespace='profiles')),

    # Recruiter dashboard
    url(r'^recruiter/', include('viking.recruiter.urls', namespace='recruiter')),

    # Reports
    url(r'^reports/', include('viking.reports.urls', namespace='reports')),

    # Search
    url(r'^search-preferences/', include('viking.searches.urls', namespace='searches')),

    # API
    url(r'^api/1/', include('viking.api.urls')),
)

# Serving static/media under debug
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
