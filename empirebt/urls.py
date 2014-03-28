from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout


urlpatterns = patterns('django.views.generic.simple',

    #Login and Logout
    url(r'^login/$',  login ),
    url(r'^logout/$', logout, {'next_page' : '/'}),

    url(r'', include('empirebt.main.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
