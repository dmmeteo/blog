from django.conf.urls import url
from . import views

urlpatterns = [
	# all posts
	url(r'^$', views.post_list, name='post_list'),
	# detail
	url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),

	# create new
	url(r'^post/new/$', views.post_new, name='post_new'),
	# edit
	url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
	# likes
	url(r'^post/(?P<pk>[0-9]+)/like/$', views.add_like, name='add_like'),
]
