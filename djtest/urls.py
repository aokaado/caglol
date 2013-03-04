from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'djtest.views.home', name='home'),
    #url(r'^djtest/', include('djtest.foo.urls')),
    url(r'^$', 'league.views.leagues'),

    url(r'^league/$', 'league.views.leagues'),
    url(r'^league/(?P<league_id>\d+)/$', 'league.views.league'),

    url(r'^player/$', 'league.views.players'),
    url(r'^player/(?P<player_id>\d+)/$', 'league.views.player'),

    url(r'^teams/$', 'league.views.teams'),
    url(r'^teams/(?P<start>\d+)/$', 'league.views.teams'),
    url(r'^team/(?P<team_id>\d+)/$', 'league.views.team'),
    url(r'^match/$', 'league.views.matches'),
    url(r'^match/(?P<match_id>\d+)/$', 'league.views.match'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Smart select app
    url(r'^chaining/', include('smart_selects.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'})
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
    }),
    )