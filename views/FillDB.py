# -*- coding: utf-8 -*-

from django.db import connection
from django.http import JsonResponse

def fillDB(request):

	#fillUser()
	#fillFollower()
	#fillForum()
	#fillThread()
	#fillPost()
	
	code = 0
	response = { "code": code, "response": "OK"}

	return JsonResponse(response)	

def fillUser():
	cursor = connection.cursor()

	query = '''insert into User 
				(username, about, isAnonymous, name, email) 
				values ('%s','%s','%d','%s','%s');
			''' % ("iproha94", "iu7", 0, "Ilya", "email1")
	cursor.execute(query)

	query = '''insert into User 
				(username, about, isAnonymous, name, email) 
				values ('%s','%s','%d','%s','%s');
			''' % ("login1", "iu3", 0, "Ivan", "email2")
	cursor.execute(query)

	query = '''insert into User 
				(username, about, isAnonymous, name, email) 
				values ('%s','%s','%d','%s','%s');
			''' % ("login2", "iu3", 1, "Vova", "email3")
	cursor.execute(query)

	query = '''insert into User 
				(username, about, isAnonymous, name, email) 
				values ('%s','%s','%d','%s','%s');
			''' % ("login3", "iu3", 0, "Sasha", "email4")
	cursor.execute(query)

	return	

def fillFollower():
	cursor = connection.cursor()

	query = '''insert into Follower 
				(followerEmail, followeeEmail) 
				values ('%s','%s');
			''' % ("email1", "email2")
	cursor.execute(query)

	query = '''insert into Follower 
				(followerEmail, followeeEmail) 
				values ('%s','%s');
			''' % ("email1", "email3")
	cursor.execute(query)

	query = '''insert into Follower 
				(followerEmail, followeeEmail) 
				values ('%s','%s');
			''' % ("email1", "email4")
	cursor.execute(query)

	query = '''insert into Follower 
				(followerEmail, followeeEmail) 
				values ('%s','%s');
			''' % ("email3", "email1")
	cursor.execute(query)

	query = '''insert into Follower 
				(followerEmail, followeeEmail) 
				values ('%s','%s');
			''' % ("email3", "email2")
	cursor.execute(query)

	return


def fillForum():
	cursor = connection.cursor()

	query = '''insert into Forum 
				(userEmail, shortName, name) 
				values ('%s','%s','%s');
			''' % ("email1", "forum1", "name_forum1")
	cursor.execute(query)

	query = '''insert into Forum 
				(userEmail, shortName, name) 
				values ('%s','%s','%s');
			''' % ("email1", "forum2", "name_forum2")
	cursor.execute(query)

	query = '''insert into Forum 
				(userEmail, shortName, name) 
				values ('%s','%s','%s');
			''' % ("email2", "forum3", "name_forum3")
	cursor.execute(query)

	query = '''insert into Forum 
				(userEmail, shortName, name) 
				values ('%s','%s','%s');
			''' % ("email1", "forum4", "name_forum4")
	cursor.execute(query)

	return

def fillThread():
	cursor = connection.cursor()

	query = '''insert into Thread 
				(forumShortName, userEmail, title, slug, message,
					date, isClosed, isDeleted) 
				values ('%s','%s','%s','%s','%s',
					'%s', '%d', '%d');
			''' % ("forum1", "email2", "title---", "slug--", "message--",
					"2014-01-01 00:00:01", 0, 0)
	cursor.execute(query)

	query = '''insert into Thread 
				(forumShortName, userEmail, title, slug, message,
					date, isClosed, isDeleted) 
				values ('%s','%s','%s','%s','%s',
					'%s', '%d', '%d');
			''' % ("forum1", "email1", "title1---", "slug1--", "message1--",
					"2014-01-01 00:00:01", 0, 0)
	cursor.execute(query)

	return

def fillPost():
	cursor = connection.cursor()
	
	query = '''insert into Post 
				(threadId, userEmail, datePost, message, 
					forumShortName) 
				values (%s,%s,%s,%s, %s) '''

	cursor.execute(query, ("2", "email4", "2014-01-01 00:00:01", "messagePost3 tratata", "forum1"))

	cursor.execute(query, ("2", "email3", "2014-01-01 00:00:01", "messagePost4 tratata", "forum1"))

	
	return