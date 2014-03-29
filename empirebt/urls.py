from django.conf.urls import patterns, include, url
from empirebt.main.api import UserResource
from empirebt.main.authorization import GeneralAuthorization
import empirebt.main.views as views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

user_resource = UserResource()
general_authorization = GeneralAuthorization()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'empirebt.views.home', name='home'),
    url(r'^api/', include(user_resource.urls)),
    url(r'^authorization/general\.json', views.auth_general),
    url(r'^authorization/chat_empire\.json', views.empire_auth),
    url(r'^authorization/chat_oneonone\.json', views.oneonone_auth),
    url(r'^authorization/battle\.json', views.battle_auth),
    url(r'^chat_oneonone/connected\.json', views.connected_oneonone),
    url(r'^chat_empire/connected\.json', views.connected_empire),
    url(r'^chat_oneonone/list\.json', views.list_oneonone),
    url(r'^chat_empire/list\.json', views.list_empire),
    #url(r'^authorization/', include(general_authorization.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
