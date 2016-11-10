from django.conf.urls import url
from . import views

urlpatterns = [
    # all posts
    url(r'^$', views.post_list, name='post_list'),
    # category list
    url(r'^category/(?P<pk>[0-9]+)/$', views.category_list, name='category_list'),
    # detail
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),

    # create new post
    url(r'^post/new/$', views.post_new, name='post_new'),
    # create new category
    url(r'^category/new/$', views.category_new, name='category_new'),

    # edit post
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    # edit category
    #url(r'^category/(?P<pk>[0-9]+)/edit/$', views.category_edit, name='category_edit'),
    # edit comment
    url(r'^comment/(?P<pk>[0-9]+)/edit/$', views.comment_edit, name='comment_edit'),

    # delete post
    url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    # delete category
    #url(r'^category/(?P<pk>[0-9]+)/delete/$', views.category_delete, name='category_delete'),
    # delete comment
    url(r'^comment/(?P<pk>[0-9]+)/delete/$', views.comment_delete, name='comment_delete'),

    # likes
    url(r'^post/(?P<pk>[0-9]+)/like/$', views.add_like, name='add_like'),

    # auth
    url(r'^accounts/login/', views.login, name='login'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
]
