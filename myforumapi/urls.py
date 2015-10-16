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

from views.General import *
from views.User import *
from views.Post import *
from views.Thread import *
from views.Forum import *
from views.FillDB import *

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),

    #General
    url(r'^db/api/clear/', clear),
    url(r'^db/api/status/', status),
    url(r'^db/api/fillDB/', fillDB),

	
    #User
    url(r'^db/api/user/create/$', createUser),
    url(r'^db/api/user/details/$', detailsUser),
    url(r'^db/api/user/follow/$', followUser),
    url(r'^db/api/user/listFollowers/$', listFollowers),
    url(r'^db/api/user/listFollowing/$', listFollowing),
    url(r'^db/api/user/listPosts/$', listPosts),
    url(r'^db/api/user/unfollow/$', unfollowUser),
    url(r'^db/api/user/updateProfile/$', updateProfileUser),


    #Post
    url(r'^db/api/post/create/$', createPost),

    #Forum
    url(r'^db/api/forum/create/$', createForum),
    url(r'^db/api/forum/details/$', detailsForum),

    #Thread
    url(r'^db/api/thread/create/$', createThread),
    url(r'^db/api/thread/details/$', detailsThread),
]
