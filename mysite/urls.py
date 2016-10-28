from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	# blog app urls
	url(r'', include('blog.urls')),
	# admin urls
	url(r'^admin/', include(admin.site.urls)),
]
