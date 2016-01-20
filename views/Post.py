# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection

from views.Forum import getInfoForum
from views.Thread import getInfoThread
from views.Forum import getInfoForumTest
from views.Thread import getInfoThreadTest
import json
from datetime import datetime


from django.views.decorators.csrf import csrf_exempt

def getThreadByPost(id, related, cursor):
	id = int(id)

	query = '''select threadId
				from Post
				where postId = %s limit 1 ;
			''' % (id) 

	cursor.execute(query)
	rowPost = cursor.fetchone()

	threadId = rowPost[0]

	return threadId

def getInfoPostTest(id, related, cursor):
	id = int(id)

	query = '''select postId
				from Post
				where postId = %s limit 1 ;
			''' % (id) 

	cursor.execute(query)

	# from views.User import getInfoUserTest

	# if 'user' in related:
	# 	getInfoUserTest(userEmail, ['followers', 'following', 'subscriptions'], cursor)	

	# del getInfoUserTest
	
	# if 'forum' in related:
	# 	getInfoForumTest(forumShortName, [], cursor)
	
	# if 'thread' in related:
	# 	getInfoThreadTest(threadId, [], cursor)

def getInfoPost(id, related, cursor):
	id = int(id)

	query = '''select threadId, userEmail, parent, datePost, message, 
					isEdited, isDeleted, isSpam, isHighlighted, isApproved,
					forumShortName, likes, dislikes, likes - dislikes
				from Post
				where postId = %s limit 1 ;
			''' % (id) 

	cursor.execute(query)
	rowPost = cursor.fetchone()

	isEdited = True if rowPost[5] == 1 else False
	isDeleted = True if rowPost[6] == 1 else False
	isSpam = True if rowPost[7] == 1 else False
	isHighlighted = True if rowPost[8] == 1 else False
	isApproved = True if rowPost[9] == 1 else False

	userEmail = rowPost[1]
	threadId = rowPost[0]
	forumShortName = rowPost[10]

	d = { "date": datetime.strftime(rowPost[3], '%Y-%m-%d %H:%M:%S'),
			"dislikes": rowPost[12],
			"likes": rowPost[11],
			"points": rowPost[13],
	        "forum": forumShortName,
	        "id": id,
	        "isEdited": isEdited,
	        "isDeleted": isDeleted,
	        "isSpam": isSpam,
	        "isHighlighted": isHighlighted,
	        "isApproved": isApproved,
	        "message": rowPost[4],
	        "parent": rowPost[2],
	        "thread": threadId,
	        "user": userEmail
		}


	if 'user' in related:
		from views.User import getInfoUser
		d.update({'user': getInfoUser(userEmail, ['followers', 'following', 'subscriptions'], cursor)})	
		del getInfoUser
	
	if 'forum' in related:
		d.update({'forum': getInfoForum(forumShortName, [], cursor)})
	
	if 'thread' in related:
		d.update({'thread': getInfoThread(threadId, [], cursor)})	

	return d

@csrf_exempt 
def createPost(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#обязательные POST
	date = request['date']
	threadId = request['thread']
	message = request['message']
	userEmail = request['user']
	forumShortName = request['forum']

	#опциональные POST
	parent = request.get('parent', None)
	isApproved = request.get('isApproved', False)
	isHighlighted = request.get('isHighlighted', False)
	isEdited = request.get('isEdited', False)
	isSpam = request.get('isSpam', False)
	isDeleted = request.get('isDeleted', False)

	isApproved = 1 if isApproved == True else 0
	isHighlighted = 1 if isHighlighted == True else 0
	isEdited = 1 if isEdited == True else 0
	isSpam = 1 if isSpam == True else 0
	isDeleted = 1 if isDeleted == True else 0

	query = '''insert ignore into Post 
				(threadId, userEmail, parent, datePost, message, 
					isEdited, isDeleted, isSpam, isHighlighted, isApproved,
					forumShortName) 
				values (%s,%s,%s,%s,%s,
					%s, %s, %s, %s, %s, 
					%s); '''

	try:
		cursor.execute(query, (threadId, userEmail,  parent, date, message,
					isEdited, isDeleted, isSpam, isHighlighted, isApproved,
					forumShortName))

		query = ''' select LAST_INSERT_ID() '''
		cursor.execute(query)
		id =  cursor.fetchone()[0]

		if isDeleted == 0 :
			query = ''' update Thread set posts = posts + 1, allposts = allposts + 1 where threadId = %s limit 1 '''
			cursor.execute(query, (threadId))

		code = 0
		responseMessage = getInfoPost(id, [], cursor) 

	except:
		code = 1
		responseMessage = "Parent post or thread or forum or user not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)


@csrf_exempt 
def detailsPost(request):
	cursor = connection.cursor()

	#обязательные GET
	postId = request.GET['post']	

	#опциональные
	related = request.GET.getlist('related', [])	

	try:
		responseMessage =  getInfoPost(postId, related, cursor)
		code = 0
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def listPost(request):
	cursor = connection.cursor()

	#обязательные GET
	threadId = request.GET.get('thread', None)
	forumShortName = request.GET.get('forum', None)

	#опциональные GET
	limit = request.GET.get('limit', None)
	orderDate = request.GET.get('order', 'desc')
	since = request.GET.get('since', None)

	#query = '''select postId
	#			from Post
#				where (threadId = %s or forumShortName = '%s') 
#				''' % (threadId, forumShortName) 


	query = '''select postId from Post '''

	if threadId is not None:
		query += " where threadId = %s " % (threadId)

	if forumShortName is not None:
		query += " where forumShortName = '%s' " % (forumShortName)

	if since is not None:
		query += " and datePost >= '%s' " % (since)

	query += " order by datePost %s " % (orderDate)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
		# if threadId is not None:
		# 	getInfoThreadTest(threadId, [], cursor)

		# if forumShortName is not None:
		# 	getInfoForumTest(forumShortName, [], cursor)

		cursor.execute(query)
		rowsPost = cursor.fetchall()

		d = [];
		for row in rowsPost:
			 d.append(getInfoPost(row[0], [], cursor))

		code = 0
		responseMessage = d
	except:
		code = 1
		responseMessage = "Thread or forum not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def removePost(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#Post
	postId = request['post']	


	try:
		temp = getThreadByPost(postId, [], cursor)

		query = ''' update Post set isDeleted = %s 
						where postId = %s limit 1 ;	
		 			update Thread set posts = posts - 1 
		 				where threadId = %s limit 1 ''' % (1, postId, int(temp))

		cursor.execute(query)

		responseMessage = { "post": postId }
		code = 0
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def restorePost(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#Post
	postId = request['post']	


	try:
		temp = getThreadByPost(postId, [], cursor)

		query = ''' update Post set isDeleted = %s 
						where postId = %s limit 1 ;	
		 			update Thread set posts = posts + 1 
		 				where threadId = %s limit 1 ''' % (0, postId, int(temp))
		cursor.execute(query)


		responseMessage = { "post": postId }
		code = 0
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)



@csrf_exempt 
def updatePost(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#обязательные POST
	message = request['message']
	postId = request['post']

	query = '''update Post 
				set message = %s 
				where postId = %s limit 1 ;	''' % (message, postId)
	
	try:
		cursor.execute(query)
		code = 0
		responseMessage = getInfoPost(postId, [], cursor)
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

@csrf_exempt 
def votePost(request1):
	cursor = connection.cursor()
 	request = json.loads(request1.body)	

	#обязательные POST
	vote = request['vote']
	postId = request['post']

	vote = 'likes' if vote == 1 else 'dislikes'

	query = ''' update Post 
				set %s = %s + 1
					where postId = %s limit 1 ;
				'''  % (vote, vote, postId)

	try:
		cursor.execute(query)

		code = 0
		responseMessage = getInfoPost(postId, [], cursor)
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)
