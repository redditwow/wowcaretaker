from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wowcaretaker.views.home', name='home'),
    # url(r'^wowcaretaker/', include('wowcaretaker.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # syncer
    url(r'^update/(?P<subreddit>[^/]+)/$', 'syncer.views.subreddit'),
)
