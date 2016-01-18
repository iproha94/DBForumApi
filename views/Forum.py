# -*- coding: utf-8 -*-
import json

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

def getInfoForumTest(shortname, related, cursor):
	query = '''select shortName
				from Forum
				where shortName = '%s' limit 1 ; 
			''' % (shortname)
	cursor.execute(query)

	# from views.User import getInfoUserTest

	# if 'user' in related:
	# 	getInfoUserTest(userEmail, ['followers', 'following', 'subscriptions'], cursor)	
	
	# del getInfoUserTest

def getInfoForum(shortname, related, cursor):
	query = '''select forumId, userEmail, shortName, name
				from Forum
				where shortName = '%s' limit 1 ; 
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

	from views.User import getInfoUser

	if 'user' in related:
		d.update({'user': getInfoUser(userEmail, ['followers', 'following', 'subscriptions'], cursor)})	
	
	del getInfoUser
	return d

@csrf_exempt 
def createForum(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#обязательные POST
	name = request['name']
	shortName = request['short_name']
	userEmail = request['user']

	query = '''insert ignore into Forum 
				(userEmail, shortName, name) 
				values (%s,%s,%s);'''

	try:			 
		cursor.execute(query, (userEmail, shortName, name))
		code = 0
		responseMessage =  getInfoForum(shortName, [], cursor) 
	except:
		code = 0
		responseMessage = request

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def detailsForum(request):
	cursor = connection.cursor()

	#обязательные GET
	shortName = request.GET['forum']	

	#опциональные
	related = request.GET.getlist('related', [])	

	try:			 
		code = 0
		responseMessage =  getInfoForum(shortName, related, cursor)
	except:
		code = 1
		responseMessage = "Forum not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def listUsersForum(request):
	cursor = connection.cursor()

	#обязательные GET
	shortName = request.GET['forum']	

	#опциональные GET
	limit = request.GET.get('limit', None)
	order = request.GET.get('order', 'desc')
	since_id = request.GET.get('since_id', None)

	query = '''select p.userEmail userEmail, u.name as uname, u.userId as userId
				from Post p join User u on p.userEmail = u.email
				where p.forumShortName = '%s'
				group by  uname, userId 
			''' % (shortName) 

	if since_id is not None:
		query += " and userId >= %s " % (since_id)

	query += " order by uname %s , userId %s" % (order, order)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
		#выдаст исключение, если такого  нет
		getInfoForumTest(shortName, [], cursor);

		cursor.execute(query)
		rowsUser = cursor.fetchall()

		from views.User import getInfoUser

		d = [];
		for row in rowsUser:
			 d.append(getInfoUser(row[0], ['followers', 'following', 'subscriptions'], cursor))

		del getInfoUser
		code = 0
		responseMessage = d
	except:
		code = 1
		responseMessage = "Forum not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def listPostsForum(request):
	cursor = connection.cursor()

	#обязательные GET
	shortName = request.GET['forum']	

	#опциональные GET
	limit = request.GET.get('limit', None)
	orderDate = request.GET.get('order', 'desc')
	since = request.GET.get('since', None)
	related = request.GET.getlist('related', [])

	query = '''select postId
				from Post
				where forumShortName = '%s' ''' % (shortName) 

	if since is not None:
		query += " and datePost >= '%s' " % (since)

	query += " order by datePost %s " % (orderDate)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
	#выдаст исключение, если такого  нет
		getInfoForumTest(shortName, [], cursor);

		cursor.execute(query)
		rowsPost = cursor.fetchall()

		from views.Post import getInfoPost

		d = [];
		for row in rowsPost:
			 d.append(getInfoPost(row[0], related, cursor))
		del getInfoPost
		code = 0
		responseMessage = d
	except:
		code = 1
		responseMessage = "Forum not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def listThreadsForum(request):
	cursor = connection.cursor()

	#обязательные GET
	shortName = request.GET['forum']	

	#опциональные GET
	limit = request.GET.get('limit', None)
	orderDate = request.GET.get('order', 'desc')
	since = request.GET.get('since', None)
	related = request.GET.getlist('related', [])

	query = '''select threadId
				from Thread
				where forumShortName = '%s' ''' % (shortName) 

	if since is not None:
		query += " and date >= '%s' " % (since)

	query += " order by date %s " % (orderDate)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
	#выдаст исключение, если такого  нет
		getInfoForumTest(shortName, [], cursor);

		cursor.execute(query)
		rowsThread = cursor.fetchall()

		from views.Thread import getInfoThread

		d = [];
		for row in rowsThread:
			 d.append(getInfoThread(row[0], related, cursor))

		del getInfoThread

		code = 0
		responseMessage = d
	except:
		code = 1
		responseMessage = "Forum not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)