from django.conf.urls.defaults import *

urlpatterns = patterns('caglol.userprofile.views', 
	url(r'^$', 'my_profile', name= 'myprofile'),
	##url(r'^update/$', 'update_profile', name= 'update_profile'),
	)
