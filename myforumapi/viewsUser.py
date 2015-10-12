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

	isAnonymous = 'true' if rowUser[5] == 1 else 'false'

	d = { "about": rowUser[2],
	        "email": email,
	        "id": rowUser[0],
	        "isAnonymous": isAnonymous,
	        "name": rowUser[3],
	        "username": rowUser[1]
		}

	return d

#получить полную инфу(с подписчиками, подписками на людей и темы) о пользователе по емейлу
def getFullInfoUser(email):
	cursor = connection.cursor()
	
	d = getInfoUser(email);

	query = '''select followeeEmail
				from Follower
				where followerEmail = '%s';
			''' % (email) 
	cursor.execute(query)
	rowsFollowee = cursor.fetchall()

	query = '''select followerEmail
				from Follower
				where followeeEmail = '%s';
			''' % (email) 
	cursor.execute(query)
	rowsFollower = cursor.fetchall()

	query = '''select threadId
				from Subscriber
				where userEmail = '%s';
			''' % (email) 
	cursor.execute(query)
	rowsSubscriber = cursor.fetchall()

	d.update({"following": rowsFollowee})
	d.update({"followers": rowsFollower})
	d.update({"subscriptions": rowsSubscriber})

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

	#опциональные POST
	#limit = request.GET.get('limit', '???')
	order = request.GET.get('order', 'desc')
	#since_id = request.GET.get('since_id', '???')

	query = '''select followerEmail
				from Follower
				where followeeEmail = '%s';
			''' % (email) 
	cursor.execute(query)
	rowsFollower = cursor.fetchall()

	d = [];
	for row in rowsFollower:
		 d.append(getFullInfoUser(row[0]))

	code = 0
	response = { "code": code, "response": d }

	return JsonResponse(response)