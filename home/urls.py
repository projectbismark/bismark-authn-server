from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testsetup.views.home', name='home'),
    # url(r'^testsetup/', include('testsetup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth2/missing_redirect_uri/?$',   'bismark.views.missing_redirect_uri'),
    url(r'^oauth2/authorize/?$',                'bismark.views.authorize'),
    url(r'^oauth2/token/?$',                    'oauth2app.token.handler'),
    url(r'^client/$', 'bismark.views.client'),
    url(r'^check/$', 'bismark.views.check'),
    url(r'^accounts/form/$', 'bismark.views.cont_register'),
    url(r'^$', 'bismark.views.profile'),   
    (r'^accounts/', include('email_usernames.urls')), 
    (r'^accounts/', include('registration.backends.default.urls')), 
)
