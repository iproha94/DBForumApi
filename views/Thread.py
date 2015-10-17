# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection

#from views.User import getInfoUser
#from views.Forum import getInfoForum

def setIntFild(Table, sampleField, sampleValue, setField, value, cursor):

	# query = "update %s set %s = %s where %s = %s "

	# cursor.execute(query, (Table, Field, value, sampleField, sampleValue))
	query = "update %s set isClosed = 0 where %s = %s;"	

	cursor.execute(query, (Table, sampleField, sampleValue))
	return

def getInfoThread(id, related, cursor):
	query = '''select date, forumShortName, isClosed, isDeleted, message, slug, title, userEmail, likes, dislikes, points
				from Thread
				where threadId = %s limit 1 ; '''  

	cursor.execute(query, (id))
	rowThread = cursor.fetchone()

	isClosed = True if rowThread[2] == 1 else False
	isDeleted = True if rowThread[3] == 1 else False

	forumShortName = rowThread[1]
	userEmail = rowThread[7]

	d = { "date": rowThread[0],
	        "forum": forumShortName,
	        "id": id,
	        "isClosed": isClosed,
	        "isDeleted": isDeleted,
	        "message": rowThread[4],
	        "slug": rowThread[5],
	        "title": rowThread[6],
	        "user": userEmail,
	        "dislikes": rowThread[9],
			"likes": rowThread[8],
			"points": rowThread[10],
		}

	from views.User import getInfoUser

	if 'user' in related:
		d.update({'user': getInfoUser(userEmail, ['followers', 'following', 'subscriptions'], cursor)})	

	del getInfoUser
	from views.Forum import getInfoForum

	if 'forum' in related:
		d.update({'forum': getInfoForum(forumShortName, [], cursor)})	
	del getInfoForum
	return d

def createThread(request):
	cursor = connection.cursor()

	#обязательные POST
	date = request.GET['date']
	forumShortName = request.GET['forum']
	message = request.GET['message']
	userEmail = request.GET['user']
	title = request.GET['title']
	slug = request.GET['slug']
	isClosed = request.GET.get('isClosed', 'false')

	#опциональные POST
	isDeleted = request.GET.get('isDeleted', 'false')

	isDeleted = 1 if isDeleted == 'true' else 0
	isClosed = 1 if isClosed == 'true' else 0

	query = ''' insert into Thread 
				(forumShortName, userEmail, title, slug, message, date, isClosed, isDeleted) 
				values (%s,%s,%s,%s,%s,%s,%s, %s); ''' 

	try:			 
		cursor.execute(query, (forumShortName, userEmail, title, slug, message,	date, isClosed, isDeleted))

		query = ''' select max(LAST_INSERT_ID(threadId) ) 
				from Thread '''
		cursor.execute(query)
		id =  cursor.fetchone()[0]

		code = 0
		responseMessage =  getInfoThread(id, [], cursor)
	except:
		query = ''' select max(LAST_INSERT_ID(threadId))  
				from Thread '''
		cursor.execute(query)
		id =  cursor.fetchone()[0]

		code = 0
		responseMessage = getInfoThread(id, [], cursor)

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)


def detailsThread(request):
	cursor = connection.cursor()

	#обязательные GET
	threadId = request.GET['thread']	

	related = request.GET.getlist('related', [])	

	try:
		responseMessage =  getInfoThread(threadId, related, cursor) 
		code = 0
	except:
	 	code = 1
	 	responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def listThread(request):
	cursor = connection.cursor()

	#обязательные GET
	userEmail = request.GET.get('user', '')
	forumShortName = request.GET.get('forum', '')

	#опциональные GET
	limit = request.GET.get('limit', None)
	orderDate = request.GET.get('order', 'desc')
	since = request.GET.get('since', None)

	query = '''select threadId
				from Thread
				where (userEmail = '%s' or forumShortName = '%s') 
				''' % (userEmail, forumShortName) 

	if since is not None:
		query += " and date >= '%s' " % (since)

	query += " order by date %s " % (orderDate)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
		if userEmail != '':
			getInfoUser(userEmail, [], cursor)

		from views.Forum import getInfoForum

		if forumShortName != '':
			getInfoForum(forumShortName, [], cursor)
		
		del getInfoForum
		
		cursor.execute(query)
		rowsThread = cursor.fetchall()

		d = [];
		for row in rowsThread:
			 d.append(getInfoThread(row[0], [], cursor))

		code = 0
		responseMessage = d
	except:
		code = 1
		responseMessage = "Forum or user not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def listPostsThread(request):
	cursor = connection.cursor()

	responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def openThread(request):
	cursor = connection.cursor()

	#Post
	threadId = request.GET['thread']	

	query = "update Thread set isClosed = %s where threadId = %s;"	

	try:
		getInfoThread(threadId, [], cursor)
		cursor.execute(query, (0, threadId))

		responseMessage = { "thread": threadId }
		code = 0
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def removeThread(request):
	cursor = connection.cursor()

	#Post
	threadId = request.GET['thread']	

	query = "update Thread set isDeleted = %s where threadId = %s;"	

	try:
		getInfoThread(threadId, [], cursor)
		cursor.execute(query, (1, threadId))

		responseMessage = { "thread": threadId }
		code = 0
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def restoreThread(request):
	cursor = connection.cursor()

	#Post
	threadId = request.GET['thread']	

	query = "update Thread set isDeleted = %s where threadId = %s;"	

	try:
		getInfoThread(threadId, [], cursor)
		cursor.execute(query, (0, threadId))

		responseMessage = { "thread": threadId }
		code = 0
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def subscribeThread(request):
	cursor = connection.cursor()

	#Post
	threadId = request.GET['thread']
	userEmail = request.GET['user']	

	query = '''insert into Subscriber 
				(userEmail, threadId) 
				values (%s,%s); ''' 

	try:
		getInfoThread(threadId, [], cursor)
		getInfoUser(userEmail, [], cursor)

		try:
			cursor.execute(query, (userEmail, threadId))
		except:
			code = 0

		responseMessage = { "thread": threadId, "user": userEmail}
		code = 0
	except:
		code = 1
		responseMessage = "Thread or User not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def unsubscribeThread(request):
	cursor = connection.cursor()

	#Post
	threadId = request.GET['thread']
	userEmail = request.GET['user']	

	query = '''delete from Subscriber 
				where userEmail = %s and threadId = %s ''' 

	try:
		getInfoThread(threadId, [], cursor)
		getInfoUser(userEmail, [], cursor)

		try:
			cursor.execute(query, (userEmail, threadId))
		except:
			code = 0

		responseMessage = { "thread": threadId, "user": userEmail}
		code = 0
	except:
		code = 1
		responseMessage = "Thread or User not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def updateThread(request):
	cursor = connection.cursor()

	#обязательные POST
	message = request.GET['message']
	slug = request.GET['slug']
	threadId = request.GET['thread']

	query = '''update Thread 
				set message = %s, slug = %s 
				where threadId = %s;	'''
	
	try:
		cursor.execute(query, (message, slug, threadId))
		code = 0
		responseMessage = getInfoThread(threadId, [], cursor)
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def voteThread(request):
	cursor = connection.cursor()

	#обязательные POST
	vote = request.GET['vote']
	threadId = request.GET['thread']


	query1 = '''update Thread 
				set likes = likes + 1 
				where threadId = %s'''

	query2 = '''update Thread 
				set dislikes = dislikes + 1 
				where threadId = %s'''

	
	query = '''update %s 
				set likes = likes + 1 
				where threadId = %s''' 
	cursor.execute(query % ("Thread", threadId))
	

	try:
		if vote == '1':
			cursor.execute(query1, (threadId))
		else:
			cursor.execute(query2, (threadId))

		code = 0
		responseMessage = getInfoThread(threadId, [], cursor)
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)



