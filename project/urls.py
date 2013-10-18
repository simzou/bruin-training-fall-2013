from django.contrib import admin
from contributions.views import IndexView
from django.conf.urls import patterns, include, url
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
