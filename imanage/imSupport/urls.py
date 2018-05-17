from django.conf.urls import patterns, include, url
import logging
　
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
　
logger = logging.getLogger('django.request')
　
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'imsupport.views.home', name='home'),
    # url(r'^imsupport/', include('imsupport.foo.urls')),
　
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
　
    # Uncomment the next line to enable the admin:
    url(r'^$', 'imsupport.apps.msupport.views.home', name='index'),
    url(r'^ttt/', 'imsupport.apps.msupport.views.tester', name='tester'),
    url(r'^auth/', include('imsupport.apps.msupport.auth.urls', namespace="auth")),
    url(r'^msupport/', include('imsupport.apps.msupport.urls', namespace="msupport")),
    url(r'^appman/', include('imsupport.apps.msupport.appman.urls', namespace="appman")),
    url(r'^appadmin/', include('imsupport.apps.msupport.appadmin.urls', namespace="appadmin")),
    url(r'^e2admin/', include('imsupport.apps.msupport.e2admin.urls', namespace="e2admin")),
    url(r'^helpers/', include('imsupport.apps.msupport.helpers.urls', namespace="helpers")),
    url(r'^remoteview/', include('imsupport.apps.msupport.remoteview.urls', namespace="remoteview")),
    url(r'^nremoteview/', include('imsupport.apps.msupport.nremoteview.urls', namespace="nremoteview")),
    url(r'^catalogue/', include('imsupport.apps.msupport.catalogue.urls', namespace="catalogue")),
    url(r'^engtools/', include('imsupport.apps.msupport.engtools.urls', namespace="engtools")),
    url(r'^certmgmt/', include('imsupport.apps.msupport.certmgmt.urls', namespace="certmgmt")),
    url(r'^usrrb/', include('imsupport.apps.msupport.rollbackusers.urls', namespace="rollbackusers")),
    url(r'^taskmgmt/', include('imsupport.apps.msupport.taskmgmt.urls', namespace="taskmgmt")),
    url(r'^devtools/', include('imsupport.apps.msupport.devtools.urls', namespace="devtools")),
    url(r'^orchestrations/', include('imsupport.apps.msupport.orchestrations.urls', namespace="orchestrations")),
    url(r'^status_check/', include('imsupport.apps.msupport.status_check.urls', namespace="status_check")),
    url(r'^admin/', include(admin.site.urls)),
)
