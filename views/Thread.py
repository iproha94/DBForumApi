# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection

#получить краткую инфу о пользователе по емейлу
def getInfoThread(id):
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

	query = '''insert into Thread 
				(forumShortName, userEmail, title, slug, message,
					date, isClosed, isDeleted) 
				values ('%s','%s','%s','%s','%s',
					'%s', '%d', '%d');
			''' % (forumShortName, userEmail, title, slug, message,
					date, isClosed, isDeleted)
	cursor.execute(query)

	code = 0
	response = { "code": code, "response": "getInfoThread(id)" }
	return JsonResponse(response)



def detailsThread(request):
	cursor = connection.cursor()

	#обязательные GET
	email = request.GET['user']	

	code = 0
	response = { "code": code, "response": getFullInfoUser(email) }

	return JsonResponse(response)

