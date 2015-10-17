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

from views.General import clear
from views.General import status
from views.FillDB import fillDB
from views.User import createUser
from views.User import detailsUser
from views.User import followUser
from views.User import listFollowers
from views.User import listFollowing
from views.User import listPostsUser
from views.User import unfollowUser
from views.User import updateProfileUser
from views.Forum import createForum
from views.Forum import  detailsForum
from views.Forum import listPostsForum
from views.Forum import  listThreadsForum
from views.Forum import listUsersForum
from views.Thread import createThread
from views.Thread import detailsThread
from views.Thread import  listThread
from views.Thread import listPostsThread
from views.Thread import  openThread
from views.Thread import removeThread
from views.Thread import restoreThread
from views.Thread import subscribeThread
from views.Thread import  unsubscribeThread
from views.Thread import updateThread
from views.Thread import  voteThread
from views.Post import createPost
from views.Post import detailsPost
from views.Post import listPost
from views.Post import removePost
from views.Post import restorePost
from views.Post import updatePost
from views.Post import votePost

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
    url(r'^db/api/user/listPosts/$', listPostsUser),
    url(r'^db/api/user/unfollow/$', unfollowUser),
    url(r'^db/api/user/updateProfile/$', updateProfileUser),


    #Forum
    url(r'^db/api/forum/create/$', createForum),
    url(r'^db/api/forum/details/$', detailsForum),
    url(r'^db/api/forum/listPosts/$', listPostsForum),
    url(r'^db/api/forum/listThreads/$', listThreadsForum),
    url(r'^db/api/forum/listUsers/$', listUsersForum),

    #Thread
    url(r'^db/api/thread/create/$', createThread),
    url(r'^db/api/thread/details/$', detailsThread),
    url(r'^db/api/thread/list/$', listThread),
    url(r'^db/api/thread/listPosts/$', listPostsThread),
    url(r'^db/api/thread/open/$', openThread),
    url(r'^db/api/thread/remove/$', removeThread),
    url(r'^db/api/thread/restore/$', restoreThread),
    url(r'^db/api/thread/subscribe/$', subscribeThread),
    url(r'^db/api/thread/unsubscribe/$', unsubscribeThread),
    url(r'^db/api/thread/update/$', updateThread),
    url(r'^db/api/thread/vote/$', voteThread),

    #Post
    url(r'^db/api/post/create/$', createPost),
    url(r'^db/api/post/details/$', detailsPost),
    url(r'^db/api/post/list/$', listPost),
    url(r'^db/api/post/remove/$', removePost),
    url(r'^db/api/post/restore/$', restorePost),
    url(r'^db/api/post/update/$', updatePost),
    url(r'^db/api/post/vote/$', votePost)
]
