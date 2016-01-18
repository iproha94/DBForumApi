# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

def getInfoThreadTest(id, related, cursor):
	id = int(id)
	query = '''select threadId
				from Thread
				where threadId = %s limit 1 ; ''' % (id)  

	cursor.execute(query)

	from views.User import getInfoUserTest
	if 'user' in related:
		getInfoUserTest(userEmail, ['followers', 'following', 'subscriptions'], cursor)	
	del getInfoUserTest

	from views.Forum import getInfoForumTest
	if 'forum' in related:
		getInfoForumTest(forumShortName, [], cursor)
	del getInfoForumTest

def getInfoThread(id, related, cursor):
	id = int(id)
	query = '''select date, forumShortName, isClosed, isDeleted, message, slug, title, userEmail, likes, dislikes, points, posts
				from Thread
				where threadId = %s limit 1 ; ''' % (id)  

	cursor.execute(query)
	rowThread = cursor.fetchone()

	isClosed = True if rowThread[2] == 1 else False
	isDeleted = True if rowThread[3] == 1 else False

	forumShortName = rowThread[1]
	userEmail = rowThread[7]

	d = { "date": datetime.strftime(rowThread[0], '%Y-%m-%d %H:%M:%S'),
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
			"posts": rowThread[11]
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

@csrf_exempt 
def createThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#обязательные POST
	date = request['date']
	forumShortName = request['forum']
	message = request['message']
	userEmail = request['user']
	title = request['title']
	slug = request['slug']
	isClosed = request.get('isClosed', False)

	#опциональные POST
	isDeleted = request.get('isDeleted', False)

	isDeleted = 1 if isDeleted == True else 0
	isClosed = 1 if isClosed == True else 0

	query = ''' insert ignore into Thread 
				(forumShortName, userEmail, title, slug, message, date, isClosed, isDeleted, posts, allposts) 
				values (%s,%s,%s,%s,%s,%s,%s,%s, 0, 0); ''' 

	try:			 
		cursor.execute(query, (forumShortName, userEmail, title, slug, message,	date, isClosed, isDeleted))

		query = ''' select max(LAST_INSERT_ID(threadId) ) from Thread '''
		cursor.execute(query)
		id =  cursor.fetchone()[0]

		code = 0
		responseMessage =  getInfoThread(id, [], cursor)
	except:
		code = 1
		responseMessage = "Parent forum or user not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def detailsThread(request):
	cursor = connection.cursor()

	#обязательные GET
	threadId = request.GET['thread']	

	related = request.GET.getlist('related', [])

	if "thread" in 	related:
		code = 3
	 	responseMessage = "Not valide request"
	else:
		try:
			responseMessage =  getInfoThread(threadId, related, cursor) 
			code = 0
		except:
		 	code = 1
		 	responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def listThread(request):
	cursor = connection.cursor()

	#обязательные GET
	userEmail = request.GET.get('user', None)
	forumShortName = request.GET.get('forum', None)

	#опциональные GET
	limit = request.GET.get('limit', None)
	orderDate = request.GET.get('order', 'desc')
	since = request.GET.get('since', None)

	query = '''select threadId
				from Thread	'''

	if userEmail is not None:
		query += " where userEmail = '%s' " % (userEmail)

	if 	forumShortName is not None:
		query += " where forumShortName = '%s' " % (forumShortName)

	if since is not None:
		query += " and date >= '%s' " % (since)

	query += " order by date %s " % (orderDate)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
		if userEmail is not None:
			from views.User import getInfoUserTest

			getInfoUserTest(userEmail, [], cursor)
			del getInfoUserTest

		from views.Forum import getInfoForumTest

		if forumShortName is not None:
			getInfoForumTest(forumShortName, [], cursor)
		
		del getInfoForumTest
		
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

@csrf_exempt 
def listPostsThread(request):
	cursor = connection.cursor()

	#обязательные GET
	threadId = request.GET['thread']

	#опциональные GET
	limit = request.GET.get('limit', None)
	orderDate = request.GET.get('order', 'desc')
	since = request.GET.get('since', None)
	sort = request.GET.get('sort', 'flat')


	query = '''select postId
				from Post
				where threadId = %s	''' % (threadId) 

	if since is not None:
		query += " and datePost >= '%s' " % (since)

	query += " order by datePost %s " % (orderDate)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
		getInfoThreadTest(threadId, [], cursor)

		cursor.execute(query)
		rowsPost = cursor.fetchall()

		from views.Post import getInfoPost
		d = [];
		for row in rowsPost:
			 d.append(getInfoPost(row[0], [], cursor))
		del getInfoPost

		code = 0
		responseMessage = d
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def openThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#Post
	threadId = request['thread']	

	query = "update Thread set isClosed = %s where threadId = %s limit 1 ;"	

	try:
		getInfoThreadTest(threadId, [], cursor)
		cursor.execute(query, (0, threadId))

		responseMessage = { "thread": threadId }
		code = 0
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def removeThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	threadId = request['thread']	

	query = '''update Thread set isDeleted = %s, posts = 0 where threadId = %s limit 1;
				update Post set isDeleted = %s where threadId = %s  ;'''	

	try:
		getInfoThreadTest(threadId, [], cursor)

		cursor.execute(query % (1, threadId, 1, threadId))

		responseMessage = { "thread": threadId }
		code = 0
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def restoreThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	threadId = request['thread']

	query = '''update Thread set isDeleted = %s, posts = allposts where threadId = %s limit 1 ;
				update Post set isDeleted = %s where threadId = %s ;	'''	

	try:
		getInfoThreadTest(threadId, [], cursor)

		cursor.execute(query % (0, threadId, 0, threadId))

		responseMessage = { "thread": threadId }
		code = 0
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def subscribeThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#Post
	threadId = request['thread']
	userEmail = request['user']	

	query = '''insert ignore into Subscriber 
				(userEmail, threadId) 
				values (%s,%s); ''' 

	try:
		getInfoThreadTest(threadId, [], cursor)
		from views.User import getInfoUserTest
		getInfoUserTest(userEmail, [], cursor)
		del getInfoUserTest

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

@csrf_exempt 
def unsubscribeThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#Post
	threadId = request['thread']
	userEmail = request['user']	

	query = '''delete from Subscriber 
				where userEmail = %s and threadId = %s ''' 

	try:
		getInfoThreadTest(threadId, [], cursor)
		from views.User import getInfoUserTest

		getInfoUserTest(userEmail, [], cursor)
		del getInfoUserTest
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

@csrf_exempt 
def updateThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#обязательные POST
	message = request['message']
	slug = request['slug']
	threadId = request['thread']

	query = '''update Thread 
				set message = %s, slug = %s 
				where threadId = %s limit 1 ;	'''
	
	try:
		cursor.execute(query, (message, slug, threadId))
		code = 0
		responseMessage = getInfoThread(threadId, [], cursor)
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def voteThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#обязательные POST
	vote = request['vote']
	threadId = request['thread']

	vote = 'likes' if vote == 1 else 'dislikes'

	query = '''update Thread 
				set %s = %s + 1 
				where threadId = %s limit 1 '''

	try:
		cursor.execute(query % (vote, vote, threadId))

		query = ''' update Thread set points = (likes - dislikes) where threadId = %s limit 1 '''	
		cursor.execute(query % (threadId))

		code = 0
		responseMessage = getInfoThread(threadId, [], cursor)
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)



@csrf_exempt 
def closeThread(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#Post
	threadId = request['thread']	

	query = "update Thread set isClosed = %s where threadId = %s limit 1 ;"	

	try:
		getInfoThreadTest(threadId, [], cursor)
		cursor.execute(query, (1, threadId))

		responseMessage = { "thread": threadId }
		code = 0
	except:
		code = 1
		responseMessage = "Thread not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)
