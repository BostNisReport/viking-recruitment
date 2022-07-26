# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(
        r'^$',
        views.dashboard,
        name='dashboard'
    ),
    url(r'^dashboard/(?P<sector_slug>[-\w]+)/$',
        views.dashboard_sector,
        name='dashboard-sector'),

    # Company list/new/edit
    url(r'^company/list/$',
        views.company_list_view,
        name='company-list'),
    url(r'^company/new/$',
        views.company_create,
        name='company-create'),
    url(r'^company/detail/(?P<pk>\d+)/$',
        views.company_update,
        name='company-update'),

    # Vessel list/new/edit
    url(r'^vessel/list/$',
        views.vessel_list_view,
        name='vessel-list'),
    url(r'^vessel/new/$',
        views.vessel_create,
        name='vessel-create'),
    url(r'^vessel/detail/(?P<pk>\d+)/$',
        views.vessel_update,
        name='vessel-update'),

    url(r'^job/list/$',
        views.job_list_view,
        name='job-list'),

    url(r'^job/new/$',
        views.job_create,
        name='job-create'),
    url(r'^job/detail/(?P<pk>\d+)/$',
        views.job_update,
        name='job-update'),
    url(r'^job/workflow/(?P<pk>\d+)/$',
        views.job_recruitment_workflow,
        name='job-workflow'),

    url(r'^job/workflow/candidate-update/(?P<pk>\d+)/$',
        views.job_workflow_candidate_update,
        name='job-workflow-candidate-update'),
    url(r'^job/workflow/candidate-finished/(?P<pk>\d+)/$',
        views.job_workflow_candidate_finished,
        name='job-workflow-candidate-finished'),
    url(r'^job/workflow/candidate-readd/(?P<pk>\d+)/$',
        views.job_workflow_candidate_readd,
        name='job-workflow-candidate-readd'),
    url(r'^job/workflow/candidate-delete/(?P<pk>\d+)/$',
        views.job_workflow_candidate_delete,
        name='job-workflow-candidate-delete'),

    url(
        r'^user/edit/(?P<pk>\d+)/$',
        views.recruiter_profile_edit_home,
        name='profile-edit-home'
    ),
    url(
        r'^user/edit/readonly/(?P<pk>\d+)/$',
        views.recruiter_profile_edit_home_readonly,
        name='profile-edit-home-readonly'
    ),
    url(
        r'^user/edit/(?P<pk>\d+)/(?P<section>[-\w]+)/$',
        views.recruiter_profile_edit,
        name='profile-edit'
    ),
    url(
        r'^user/edit/readonly/(?P<pk>\d+)/(?P<section>[-\w]+)/$',
        views.recruiter_profile_edit_readonly,
        name='profile-edit-readonly'
    ),
    url(
        r'^user/managed/list/$',
        views.user_managed_list,
        name='user-managed-list'
    ),
    url(
        r'^search/$',
        views.search,
        name='search'
    ),
    url(
        r'^search/candidate/$',
        views.candidate_search,
        name='candidate-search'
    ),
    url(
        r'^whiteboard/$',
        views.whiteboard,
        name='whiteboard'
    ),
)
