# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection

from views.Forum import getInfoForum
from views.Thread import getInfoThread

def getInfoPost(id, related, cursor):
	query = '''select threadId, userEmail, parent, datePost, message, 
					isEdited, isDeleted, isSpam, isHighlighted, isApproved,
					forumShortName, likes, dislikes, points
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

	d = { "date": rowPost[3],
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

	from views.User import getInfoUser

	if 'user' in related:
		d.update({'user': getInfoUser(userEmail, ['followers', 'following', 'subscriptions'], cursor)})	

	del getInfoUser
	
	if 'forum' in related:
		d.update({'forum': getInfoForum(forumShortName, [], cursor)})
	
	if 'thread' in related:
		d.update({'thread': getInfoThread(threadId, [], cursor)})	
	
	
	

	return d




def createPost(request):
	cursor = connection.cursor()

	#обязательные POST
	date = request.GET['date']
	threadId = request.GET['thread']
	message = request.GET['message']
	userEmail = request.GET['user']
	forumShortName = request.GET['forum']

	#опциональные POST
	parent = request.GET.get('parent', 'Null')
	isApproved = request.GET.get('isApproved', 'false')
	isHighlighted = request.GET.get('isHighlighted', 'false')
	isEdited = request.GET.get('isEdited', 'false')
	isSpam = request.GET.get('isSpam', 'false')
	isDeleted = request.GET.get('isDeleted', 'false')

	isApproved = 1 if isApproved == 'true' else 0
	isHighlighted = 1 if isHighlighted == 'true' else 0
	isEdited = 1 if isEdited == 'true' else 0
	isSpam = 1 if isSpam == 'true' else 0
	isDeleted = 1 if isDeleted == 'true' else 0

	query = '''insert into Post 
				(threadId, userEmail, parent, datePost, message, 
					isEdited, isDeleted, isSpam, isHighlighted, isApproved,
					forumShortName) 
				values (%s,%s,%s,%s,%s,
					%s, %s, %s, %s, %s, 
					%s); '''
	cursor.execute(query)

	try:			 
		cursor.execute(query, (threadId, userEmail, parent, date, message,
					isEdited, isDeleted, isSpam, isHighlighted, isApproved,
					forumShortName))
		code = 0
		responseMessage =  getInfoPost(shortName, [], cursor) 
	except:
		code = 0
		responseMessage = getInfoPost(shortName, [], cursor)

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)



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


def listPost(request):
	cursor = connection.cursor()

	#обязательные GET
	threadId = request.GET.get('thread', '0')
	forumShortName = request.GET.get('forum', '')

	#опциональные GET
	limit = request.GET.get('limit', None)
	orderDate = request.GET.get('order', 'desc')
	since = request.GET.get('since', None)

	query = '''select postId
				from Post
				where (threadId = %s or forumShortName = '%s') 
				''' % (threadId, forumShortName) 

	if since is not None:
		query += " and datePost >= '%s' " % (since)

	query += " order by datePost %s " % (orderDate)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
		if threadId != '0':
			getInfoThread(threadId, [], cursor)

		if forumShortName != '':
			getInfoForum(forumShortName, [], cursor)

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


def removePost(request):
	cursor = connection.cursor()

	#Post
	postId = request.GET['post']	

	query = "update Post set isDeleted = %s where postId = %s;"	

	try:
		getInfoPost(postId, [], cursor)
		cursor.execute(query, (1, postId))

		responseMessage = { "post": postId }
		code = 0
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def restorePost(request):
	cursor = connection.cursor()

	#Post
	postId = request.GET['post']	

	query = "update Post set isDeleted = %s where postId = %s;"	

	try:
		getInfoPost(postId, [], cursor)
		cursor.execute(query, (0, postId))

		responseMessage = { "post": postId }
		code = 0
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)




def updatePost(request):
	cursor = connection.cursor()

	#обязательные POST
	message = request.GET['message']
	postId = request.GET['post']

	query = '''update Post 
				set message = %s 
				where postId = %s;	'''
	
	try:
		cursor.execute(query, (message, postId))
		code = 0
		responseMessage = getInfoPost(postId, [], cursor)
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)

def votePost(request):
	cursor = connection.cursor()

	#обязательные POST
	vote = request.GET['vote']
	postId = request.GET['post']


	query1 = '''update Post 
				set likes = likes + 1 
				where postId = %s'''

	query2 = '''update Post 
				set dislikes = dislikes + 1 
				where postId = %s'''

	
	try:
		if vote == '1':
			cursor.execute(query1, (postId))
		else:
			cursor.execute(query2, (postId))

		code = 0
		responseMessage = getInfoPost(postId, [], cursor)
	except:
		code = 1
		responseMessage = "Post not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)
