# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection

from views.Post import getInfoPost

#получить инфу о пользователе по емейлу
def getInfoUser(email, related, cursor):
	query = '''select userId, username, about, name, email, isAnonymous
				from User
				where email = '%s' limit 1 ;
			''' % (email) 

	cursor.execute(query)
	rowUser = cursor.fetchone()

	isAnonymous = True if rowUser[5] == 1 else False

	d = { "about": rowUser[2],
	        "email": email,
	        "id": rowUser[0],
	        "isAnonymous": isAnonymous,
	        "name": rowUser[3],
	        "username": rowUser[1]
		}

	if 'followers' in related:
		query = '''select followerEmail
				from Follower
				where followeeEmail = '%s';
			''' % (email) 
		cursor.execute(query)
		rowsFollower = cursor.fetchall()

		a = [];
		for row in rowsFollower:
			 a.append(row[0])
		d.update({"followers": a})	

	if 'following' in related:
		query = '''select followeeEmail
				from Follower
				where followerEmail = '%s';
			''' % (email) 
		cursor.execute(query)
		rowsFollowee = cursor.fetchall()

		a = [];
		for row in rowsFollowee:
			 a.append(row[0])
		d.update({"following": a})

	if 'subscriptions' in related:
		query = '''select threadId
				from Subscriber
				where userEmail = '%s';
			''' % (email) 
		cursor.execute(query)
		rowsSubscriber = cursor.fetchall()

		a = [];
		for row in rowsSubscriber:
			 a.append(row[0])
		d.update({"subscriptions": a})

	return d

def createUser(request):
	cursor = connection.cursor()

	#обязательные POST
	username = request.GET['username']
	about = request.GET['about']
	name = request.GET['name']
	email = request.GET['email']

	#опциональные POST
	isAnonymous = request.GET.get('isAnonymous', 'false')

	isAnonymous = 1 if isAnonymous == 'true' else 0

	query = '''insert into User 
				(username, about, isAnonymous, name, email) 
				values ('%s','%s','%d','%s','%s');
			''' % (username, about, isAnonymous, name, email)
	
	try:
		cursor.execute(query)
		code = 0
		responseMessage = getInfoUser(email, [], cursor)
	except:
		code = 5
		responseMessage = "User already exists"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)



def detailsUser(request):
	cursor = connection.cursor()

	#обязательные GET
	email = request.GET['user']	

	try:
		response =  getInfoUser(email, ['followers', 'following', 'subscriptions'], cursor)
		code = 0
	except:
		code = 1
		response = "User not found"

	response = { "code": code, "response": response}
	return JsonResponse(response)

def followUser(request):
	cursor = connection.cursor()

	#обязательные POST
	followerEmail = request.GET['follower']		
	followeeEmail = request.GET['followee']

	query = '''insert into Follower 
				(followerEmail, followeeEmail) 
				values ('%s','%s');
			''' % (followerEmail, followeeEmail)

	try:
		cursor.execute(query)
		code = 0
		response = getInfoUser(followerEmail, ['followers', 'following', 'subscriptions'], cursor)
	except:
		code = 1
		response = "User not found"

	response = { "code": code, "response": response}
	return JsonResponse(response)

def listFollowers(request):
	cursor = connection.cursor()

	#обязательные GET
	email = request.GET['user']	

	#опциональные GET
	limit = request.GET.get('limit', None)
	order = request.GET.get('order', 'desc')
	since_id = request.GET.get('since_id', None)

	query = '''select fer.followerEmail, u.name followerName, u.userId followerId
				from Follower fer, User u
				where u.email = fer.followerEmail 
					and fer.followeeEmail = '%s'
			''' % (email) 

	if since_id is not None:
		query += " and followerId >= %s " % (since_id)

	query += " order by followerName %s " % (order)

	if limit is not None:
		query += " limit %s " % (limit)

	try:
		#выдаст исключение, если такого пользователя нет
		getInfoUser(email, [], cursor);

		cursor.execute(query)
		rowsFollower = cursor.fetchall()

		d = [];
		for row in rowsFollower:
			 d.append(getInfoUser(row[0], ['followers', 'following', 'subscriptions'], cursor))

		code = 0
		response = d
	except:
		code = 1
		response = "User not found"

	response = { "code": code, "response": response}
	return JsonResponse(response)

def listFollowing(request):
	cursor = connection.cursor()

	#обязательные GET
	email = request.GET['user']	

	#опциональные GET
	limit = request.GET.get('limit', None)
	order = request.GET.get('order', 'desc')
	since_id = request.GET.get('since_id', None)

	query = '''select fee.followeeEmail, u.name followeeName, u.userId
				from Follower fee, User u
				where u.email = fee.followeeEmail 
					and fee.followerEmail = '%s'
			''' % (email) 

	if since_id is not None:
		query += " and userId >= %s " % (since_id)

	query += " order by followeeName %s " % (order)

	if limit is not None:
		query += " limit %s " % (limit)
		
	try:
		#выдаст исключение, если такого пользователя нет
		getInfoUser(email, [], cursor);

		cursor.execute(query)
		rowsFollowee = cursor.fetchall()

		d = [];
		for row in rowsFollowee:
			 d.append(getInfoUser(row[0], ['followers', 'following', 'subscriptions'], cursor))

		code = 0
		response = d
	except:
		code = 1
		response = "User not found"

	response = { "code": code, "response": response}
	return JsonResponse(response)


def unfollowUser(request):
	cursor = connection.cursor()

	#обязательные POST
	followerEmail = request.GET['follower']		
	followeeEmail = request.GET['followee']

	query = '''delete from Follower 
				where followerEmail = %s and followeeEmail = %s ;'''

	try:
		cursor.execute(query, (followerEmail, followeeEmail))
		code = 0
		response = getInfoUser(followerEmail, ['followers', 'following', 'subscriptions'], cursor)
	except:
		code = 1
		response = "User not found"

	response = { "code": code, "response": response}
	return JsonResponse(response)

def updateProfileUser(request):
	cursor = connection.cursor()

	#обязательные POST
	about = request.GET['about']
	name = request.GET['name']
	email = request.GET['user']

	query = '''update User 
				set about = %s, name = %s 
				where email = %s;	'''
	
	try:
		cursor.execute(query, (about, name, email))
		code = 0
		response = getInfoUser(email, ['followers', 'following', 'subscriptions'], cursor)
	except:
		code = 1
		response = "User not found"

	response = { "code": code, "response": response}
	return JsonResponse(response)

def listPostsUser(request):
	cursor = connection.cursor()

	#обязательные GET
	userEmail = request.GET['user']

	#опциональные GET
	limit = request.GET.get('limit', None)
	orderDate = request.GET.get('order', 'desc')
	since = request.GET.get('since', None)

	query = '''select postId
				from Post
				where userEmail = '%s' 
				''' % (userEmail) 

	if since is not None:
		query += " and datePost >= '%s' " % (since)

	query += " order by datePost %s " % (orderDate)

	if limit is not None:
		query += " limit %s " % (limit)
		
	# try:
	getInfoUser(userEmail, [], cursor)

	cursor.execute(query)
	rowsPost = cursor.fetchall()

	d = [];
	for row in rowsPost:
		 d.append(getInfoPost(row[0], [], cursor))

	code = 0
	responseMessage = d
	# except:
	# 	code = 1
	# 	responseMessage = "User not found"

	response = { "code": code, "response": responseMessage}
	return JsonResponse(response)