# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection

#получить краткую инфу о пользователе по емейлу
def getInfoUser(email):
	cursor = connection.cursor()
	
	query = '''select userId, username, about, name, email, isAnonymous
				from User
				where email = '%s';
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

	return d



#получить полную инфу(с подписчиками(емайл), подписками на людей(емайл) и темы(id)) о пользователе по емейлу
def getFullInfoUser(email):
	cursor = connection.cursor()
	
	d = getInfoUser(email);

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
	cursor.execute(query)

	code = 0
	response = { "code": code, "response": getInfoUser(email) }
	return JsonResponse(response)



def detailsUser(request):
	cursor = connection.cursor()

	#обязательные GET
	email = request.GET['user']	

	code = 0
	response = { "code": code, "response": getFullInfoUser(email) }

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
	cursor.execute(query)

	code = 0
	response = { "code": code, "response": getFullInfoUser(followerEmail) }

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
		
	cursor.execute(query)
	rowsFollower = cursor.fetchall()

	d = [];
	for row in rowsFollower:
		 d.append(getFullInfoUser(row[0]))

	code = 0
	response = { "code": code, "response": d }

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
		
	cursor.execute(query)
	rowsFollowee = cursor.fetchall()

	d = [];
	for row in rowsFollowee:
		 d.append(getFullInfoUser(row[0]))

	code = 0
	response = { "code": code, "response": d }

	return JsonResponse(response)


def listPosts(request):

	response = { "code": 0, "response": [] }

	return JsonResponse(response)

