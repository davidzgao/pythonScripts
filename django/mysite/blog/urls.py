# -*- coding:utf8 -*-
from django.conf.urls import patterns, include, url
#from blog.views import *

urlpatterns = patterns('blog.views',
    url(r'^$', 'home'),
    url(r'^create/', 'create_blogpost'),
    url(r'^home/', 'home'),
    url(r'^(?P<id>\d+)/$', 'detail', name= 'detail'),
    url(r'^aboutme/', 'aboutme'),
    url(r'^tag:(?P<tag>\w+)/$', 'search_tag_func', name = 'search_tag'),   # first_arg defines url, second defines func in views.py , third_arg defines url name in html ,which means "href="{% url "search_tag" tag=post.category %}""
    url(r'^search/$' ,'search_func', name = 'search'),
)
