from django.conf.urls import url

from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'thesite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'rmxbot.apps.data.views.get_data'),

    url(r'^create/$', views.create),

    url(r'^crawl-ready/(?P<corpusid>[0-9a-zA-Z]*)/$', views.crawl_ready),



]
