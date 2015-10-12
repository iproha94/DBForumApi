# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection

def clear(request):
	cursor = connection.cursor()

	query = '''delete from Subscriber;
				delete from Follower;
				delete from Post;
				delete from Thread; 
				delete from Forum;
				delete from User;
			'''

	cursor.execute(query)

	code = 0
	mess = "OK"
	response = { "code": code, "response": mess }

	return JsonResponse(response)

def status(request):
	cursor = connection.cursor()

	query = '''select count(*) from User;'''
	cursor.execute(query)
	sizeUser = cursor.fetchone()[0]

	query = '''select count(*) from Thread;'''
	cursor.execute(query)
	sizeThread = cursor.fetchone()[0]

	query = '''select count(*) from Forum;'''
	cursor.execute(query)
	sizeForum = cursor.fetchone()[0]

	query = '''select count(*) from Post;'''
	cursor.execute(query)
	sizePost = cursor.fetchone()[0]

	d = {"user": sizeUser, "thread": sizeThread, "forum": sizeForum, "post": sizePost}
	code = 0
	response = { "code": code, "response": d }

	return JsonResponse(response)	