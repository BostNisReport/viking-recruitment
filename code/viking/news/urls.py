from django.conf.urls import patterns, url
from blanc_basic_news.urls import urlpatterns as news_urlpatterns
from blanc_basic_news import views


urlpatterns = patterns('',
    url(r'^$',
        views.PostListView.as_view(
            template_name='news/post_list_frontpage.html',
            paginate_by=None),
        name='post-list-frontpage'),
    url(r'^archive/$',
        views.PostListView.as_view(),
        name='post-list-archive'),
)

urlpatterns += news_urlpatterns
