# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.db import connection

def getInfoPost(id):
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
				values ('%s','%s',%s,'%s','%s',
					'%d', '%d', '%d', '%d', '%d', 
					'%s');
			''' % (threadId, userEmail, parent, date, message,
					isEdited, isDeleted, isSpam, isHighlighted, isApproved,
					forumShortName)
	cursor.execute(query)

	code = 0
	response = { "code": code, "response": "getInfoPost(id)" }
	return JsonResponse(response)



def detailsPost(request):
	cursor = connection.cursor()

	#обязательные GET
	email = request.GET['user']	

	code = 0
	response = { "code": code, "response": getFullInfoUser(email) }

	return JsonResponse(response)

