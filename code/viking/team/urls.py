from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$',
        views.GroupDetailView.as_view(),
        name='group-detail'),
    url(r'^profile/(?P<slug>[-\w]+)/$',
        views.ProfileDetailView.as_view(),
        name='profile-detail'),
)
