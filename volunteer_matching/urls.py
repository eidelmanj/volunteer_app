from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'volunteer_matching.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^social/', include('social_network.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
