# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection
from myforumapi.viewsUser import getFullInfoUser

def getInfoForum(shortname, related):
	cursor = connection.cursor()

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
		d.update({'user': getFullInfoUser(userEmail)})	
	
	return d

def createForum(request):
	cursor = connection.cursor()

	#обязательные POST
	name = request.GET['name']
	shortName = request.GET['short_name']
	userEmail = request.GET['user']

	query = '''insert into Forum 
				(userEmail, shortName, name) 
				values ('%s','%s','%s');
			''' % (userEmail, shortName, name)
	cursor.execute(query)

	code = 0
	response = { "code": code, "response": getInfoForum(shortName, related) }
	return JsonResponse(response)

def detailsForum(request):
	cursor = connection.cursor()

	#обязательные GET
	shortName = request.GET['forum']	

	#опциональные
	related = request.GET.getlist('related', [])	

	code = 0
	response = { "code": code, "response": getInfoForum(shortName, related) }

	return JsonResponse(response)

