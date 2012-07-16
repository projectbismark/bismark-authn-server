from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testsetup.views.home', name='home'),
    # url(r'^testsetup/', include('testsetup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^account/login', include(admin.site.urls)),
    url(r'^oauth2/missing_redirect_uri/?$',   'oauth2.views.missing_redirect_uri'),
    url(r'^oauth2/authorize/?$',                'oauth2.views.authorize'),
    url(r'^oauth2/token/?$',                    'oauth2app.token.handler'),
    url(r'^client/$', 'oauth2.views.client'),
    url(r'^check/$', 'oauth2.views.check'),
    url(r'^register/$', 'oauth2.views.cont_register'),
    url(r'^accounts/profile/$', 'oauth2.views.profile'),  
    (r'^accounts/', include('registration.backends.default.urls')),
)
