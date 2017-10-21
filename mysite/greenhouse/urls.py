from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),
    # /video/
    url(r'^video/$', views.video, name='video'),
    # /contact/
    url(r'^contact/$', views.contact, name='contact'),
    # /about/
    url(r'^about/$', views.about, name='about'),
    # /detailed/
    url(r'^detailed/$', views.redirect, name='redirect'),
    # /detailed/temperature/
    url(r'^detailed/(?P<detailed_url>[a-z]+)/$',
        views.detailed,
        name='detailed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
