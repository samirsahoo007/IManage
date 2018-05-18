from django.conf.urls import patterns, url
　
from imSupport.apps.msupport import views
　
urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^ttt/$', views.tester, name='tester'),
　
)
