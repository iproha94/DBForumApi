"""myforumapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from myforumapi.viewsGeneral import *
from myforumapi.viewsUser import *
from myforumapi.viewsPost import *
from myforumapi.viewsThread import *
from myforumapi.viewsForum import *
from myforumapi.autoFillDB import *

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),

	#Fill
	url(r'^db/api/user/fillUser/', fillUser),
	url(r'^db/api/user/fillFollower/', fillFollower),
	url(r'^db/api/forum/fillForum/', fillForum),
	url(r'^db/api/thread/fillThread/', fillThread),
	url(r'^db/api/post/fillPost/', fillPost),

    #General
    url(r'^db/api/clear/', clear),
    url(r'^db/api/status/', status),
	
    #User
    url(r'^db/api/user/create/$', createUser),
    url(r'^db/api/user/details/$', detailsUser),
    url(r'^db/api/user/follow/$', followUser),
    url(r'^db/api/user/listFollowers/$', listFollowers),
    url(r'^db/api/user/listFollowing/$', listFollowing),
    url(r'^db/api/user/listPosts/$', listPosts),

    #Post
    url(r'^db/api/post/create/$', createPost),

    #Forum
    url(r'^db/api/forum/create/$', createForum),
    url(r'^db/api/forum/details/$', detailsForum),

    #Thread
    url(r'^db/api/thread/create/$', createThread),
    url(r'^db/api/thread/details/$', detailsThread),
]
