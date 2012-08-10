from django.conf.urls import patterns, include, url
import django.contrib.auth.views
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
    url(r'^oauth2/missing_redirect_uri/?$',   'bismark-app.views.missing_redirect_uri'),
    url(r'^oauth2/authorize/?$',                'bismark-app.views.authorize'),
    url(r'^oauth2/token/?$',                    'oauth2app.token.handler'),
    url(r'^client/$', 'bismark-app.views.client'),
    url(r'^check/$', 'bismark-app.views.check'),
    url(r'^accounts/form/$', 'bismark-app.views.cont_register'),
    url(r'^$', 'bismark-app.views.profile'), 
    url(r'^router/$', 'bismark-app.views.router'), 
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^accounts/', include('email_usernames.urls')), 
    (r'^accounts/', include('registration.backends.default.urls')), 
)
