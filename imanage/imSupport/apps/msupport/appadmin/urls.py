from django.conf.urls import patterns, url
　
from imSupport.apps.msupport.appadmin import views
　
urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'grant/$', views.grant_view, name="grant_view"),
    url(r'grant/action/$', views.grant_action, name="grant_action"),
    url(r'revoke/$', views.revoke, name="revoke"),
　
"""
    url(r'application/add/$', views.ApplicationCreate.as_view(), name='application_add'),
    url(r'application/(?P<pk>.*)/$', views.ApplicationUpdate.as_view(), name='application_update'),
    url(r'application/(?P<pk>.*)/delete/$', views.ApplicationDelete.as_view(), name='application_delete'),
　
    url(r'environment/$', views.EnvironmentList.as_view(), name="environment_list"),
    url(r'environment/add/$', views.EnvironmentCreate.as_view(), name='environment_add'),
    url(r'environment/(?P<pk>.*)/$', views.EnvironmentUpdate.as_view(), name='environment_update'),
    url(r'environment/(?P<pk>.*)/delete/$', views.EnvironmentDelete.as_view(), name='environment_delete'),
　
    url(r'server/$', views.ServerList.as_view(), name="server_list"),
    url(r'server/add/$', views.ServerCreate.as_view(), name='server_add'),
    url(r'server/(?P<pk>.*)/$', views.ServerUpdate.as_view(), name='server_update'),
    url(r'server/(?P<pk>.*)/delete/$', views.ServerDelete.as_view(), name='server_delete'),
　
    url(r'instance/$', views.InstanceList.as_view(), name="instance_list"),
    url(r'instance/add/$', views.InstanceCreate.as_view(), name='instance_add'),
    url(r'instance/(?P<pk>.*)/$', views.InstanceUpdate.as_view(), name='instance_update'),
    url(r'instance/(?P<pk>.*)/delete/$', views.InstanceDelete.as_view(), name='instance_delete'),
　
    url(r'product/$', views.ProductList.as_view(), name="product_list"),
    url(r'product/add/$', views.ProductCreate.as_view(), name='product_add'),
    url(r'product/(?P<pk>.*)/$', views.ProductUpdate.as_view(), name='product_update'),
    url(r'product/(?P<pk>.*)/delete/$', views.ProductDelete.as_view(), name='product_delete'),
　
    url(r'contact/$', views.ContactList.as_view(), name="contact_list"),
    url(r'contact/add/$', views.ContactCreate.as_view(), name='contact_add'),
    url(r'contact/(?P<pk>.*)/$', views.ContactUpdate.as_view(), name='contact_update'),
    url(r'contact/(?P<pk>.*)/delete/$', views.ContactDelete.as_view(), name='contact_delete'),
　
    url(r'url/$', views.URLList.as_view(), name="url_list"),
    url(r'url/add/$', views.URLCreate.as_view(), name='url_add'),
    url(r'url/(?P<pk>.*)/$', views.URLUpdate.as_view(), name='url_update'),
    url(r'url/(?P<pk>.*)/delete/$', views.URLDelete.as_view(), name='url_delete'),
"""
)
