from django.conf.urls import patterns, url
　
from imSupport.apps.msupport.appman import views, views_mq, views_ora
　
urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^confirm_action/$', views.confirm_action, name='confirm_action'),
    url(r'^action/$', views.action, name='action'),
    url(r'^ora/listinst/$', views_ora.listinst, name='ora_listinst'),
    url(r'^ora/oratools/$', views_ora.oratools, name='ora_tools'),
    url(r'^mq/dispqmgr/$', views_mq.dispqmgr, name='dispqmgr'),
    url(r'^mq/getqmgr/$', views_mq.getqmgr, name='getqmgr'),
    url(r'^mq/dispmqver/$', views_mq.dispmqver, name='dispmqver'),
    url(r'^mq/dispchannel/$', views_mq.dispchannel, name='dispchannel'),
    url(r'^mq/dispchannelstatus/$', views_mq.dispchannelstatus, name='dispchannelstatus'),
    url(r'^mq/dispq/$', views_mq.dispq, name='dispq'),
    url(r'^mq/mqtools/$', views_mq.mqtools, name='mqtools'),
　
