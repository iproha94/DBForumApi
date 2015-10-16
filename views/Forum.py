# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection
from views.User import getInfoUser

def getInfoForum(shortname, related, cursor):
	query = '''select forumId, userEmail, shortName, name
				from Forum
				where shortName = '%s'; 
			''' % (shortname)
	cursor.execute(query)

	rowForum = cursor.fetchone()

	forumId = rowForum[0]
	userEmail = rowForum[1]
	name = rowForum[3]
	shortname = rowForum[2]

	d = { "id": forumId,
	        "user": userEmail,
	        "name": name,
	        "short_name": shortname
		}

	if 'user' in related:
		d.update({'user': getInfoUser(userEmail, ['followers', 'following', 'subscriptions'], cursor)})	
	
	return d

def createForum(request):
	cursor = connection.cursor()

	#обязательные POST
	name = request.GET['name']
	shortName = request.GET['short_name']
	userEmail = request.GET['user']

	query = '''insert into Forum 
				(userEmail, shortName, name) 
				values (%s,%s,%s);'''

	try:			 
		cursor.execute(query, (userEmail, shortName, name))
		code = 0
		responseMessage =  getInfoForum(shortName, [], cursor) 
	except:
		code = 0
		responseMessage = getInfoForum(shortName, [], cursor)

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def detailsForum(request):
	cursor = connection.cursor()

	#обязательные GET
	shortName = request.GET['forum']	

	#опциональные
	related = request.GET.getlist('related', [])	

	code = 0
	response = { "code": code, "response": getInfoForum(shortName, related, cursor) }

	return JsonResponse(response)

