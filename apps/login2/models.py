from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

letter_regex = re.compile(r'[a-zA-Z]*$')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
	def rvalidate(self, postData):
		errors = []

		flag = False # no errors at this time
		if not postData['first_name']:
			errors.append("First name must not be blank")
			flag = True 
		if len(postData['first_name']) < 2:
			errors.append("First name must not be less than 2")
			flag = True
		if not letter_regex.match(postData['first_name']):
			errors.append("First name can not be blank")
			flag = True





		if not postData['last_name']:
			errors.append("Last name must not be blank")
			flag = True 
		if len(postData['last_name']) < 2:
			errors.append("Last name must not be less than 2")
			flag = True
		if not letter_regex.match(postData['last_name']):
			errors.append("Last name can not be blank")
			flag = True




		if not postData['email']:
			errors.append("Email must not be blank")
			flag = True 

		if not email_regex.match(postData['email']):
			errors.append("Email is not valid")
			flag = True
		




		if not postData['password']:
			errors.append("Password must not be blank")
			flag = True 

		if postData['password'] != postData['confirm_pw']:
			errors.append("Password must match")
			flag = True

		if len(postData['password']) < 8:
			errors.append('Password must have 8 characters!')
			flag = True

		if not flag:
			hashedPw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			if User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashedPw):

				user = User.objects.last()
				return (flag, user)
			else:

				return (flag, errors)

	def lvalidate(self, postData):
		try:
			user = User.objects.get(email = postData['email'])
			password = postData['password'].encode()
			hashed = user.password.encode()

			if bcrypt.hashpw(password, hashed) == hashed and user:
				return (True, user)

		except:

			return (False, " Login credentials are invalid")




class User(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45)
	email = models.CharField(max_length = 45)
	password = models.CharField(max_length = 45)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()