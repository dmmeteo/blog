from django.conf.urls import url
from . import views

urlpatterns = [
    # all posts
    url(r'^$', views.post_list, name='post_list'),
    url(r'^page/(?P<page_number>\d+)/$', views.post_list, name='post_list_pages'),
    # category list
    url(r'^category/(?P<pk>\d+)/$', views.category_list, name='category_list'),
    url(r'^category/(?P<pk>\d+)/page/(?P<page_number>\d+)/$', views.category_list, name='category_list_pages'),

    # detail
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),

    # create new post
    url(r'^post/new/$', views.post_new, name='post_new'),
    # create new category
    url(r'^category/new/$', views.category_new, name='category_new'),

    # edit post
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    # edit category
    url(r'^category/(?P<pk>\d+)/edit/$', views.category_edit, name='category_edit'),
    # edit comment
    url(r'^comment/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),

    # delete post
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    # delete category
    url(r'^category/(?P<pk>\d+)/delete/$', views.category_delete, name='category_delete'),
    # delete comment
    url(r'^comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),

    # likes
    url(r'^post/(?P<pk>\d+)/like/$', views.add_like, name='add_like'),

    # auth
    url(r'^accounts/login/', views.login, name='login'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/password/new/$', views.password_change, name='password_change'),
]
