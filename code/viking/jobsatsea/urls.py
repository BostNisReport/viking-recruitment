from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',
        views.jobsatsea_home,
        name='home'),
    url(r'^search/$',
        views.jobsatsea_search,
        name='job-search'),
    url(r'^search/(?P<sector_slug>[-\w]+)/$',
        views.jobsatsea_sector,
        name='job-search-sector'),
    url(r'^search/(?P<sector_slug>[-\w]+)/(?P<department_slug>[-\w]+)/$',
        views.jobsatsea_category,
        name='job-search'),
    url(r'^view/(?P<pk>\d+)/$',
        views.jobsatsea_detail,
        name='job-detail'),
    url(r'^apply/(?P<pk>\d+)/$',
        views.jobsatsea_apply,
        name='job-apply'),
    url(r'^thanks/$',
        views.jobsatsea_thanks,
        name='form-thanks'),
]
