from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # apps urls
    url(r'', include('blog.urls')),
    url(r'sender/', include('sender.urls')),
    # admin urls
    url(r'^admin/', include(admin.site.urls)),
]
