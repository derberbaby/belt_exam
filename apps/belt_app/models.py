# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re
import datetime
import dateutil.relativedelta
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register(self, userData):
		messages = []

		for field in userData:
			if len(userData[field]) == 0:
				fields = {
					'name':'Name',
					'username':'Username',
					'password':'Password',
					'confirm_pw':'Confirm Password',
				}
				messages.append(fields[field]+' must be filled in')

		if len(userData['name']) < 3:
			messages.append('Name must be at least three characters long')

		if len(userData['username']) < 3:
			messages.append('Username must be at least three characters long')

		# if userData['first_name'].isalpha()==False or userData['last_name'].isalpha()==False:
		# 	messages.append('Name must only contain letters')

		# if not EMAIL_REGEX.match(userData['email']):
		# 	messages.append('Must enter a valid email')

		try:
			User.objects.get(username=userData['username'])
			messages.append('Username already registered')
		except:
			pass

		if len(userData['password']) < 8:
			messages.append('Password must be at least eight characters long')

		# if re.search('[0-9]', userData['password']) is None:
		# 	messages.append('Password must contain at least one number')
        #
		# if re.search('[A-Z]', userData['password']) is None:
		# 	messages.append('Password must contain at least one capital letter')

		if userData['password'] != userData['confirm_pw']:
			messages.append('Password and confirm password must match')

		if len(messages) > 0:
			return messages
		else:
			hashed_pw=bcrypt.hashpw(userData['password'].encode(), bcrypt.gensalt())
			new_user= User.objects.create(name=userData['name'], username=userData['username'], hashed_pw=hashed_pw)
			return new_user.id

	def login(self, userData):
		messages = []
		for field in userData:
			if len(userData[field]) == 0:
				fields = {
					'username':'Username',
					'password':'Password'
				}
				messages.append(fields[field]+' must be filled in')

		try:
			user = User.objects.get(username=userData['username'])
			encrypted_pw = bcrypt.hashpw(userData['password'].encode(), user.hashed_pw.encode())
			if encrypted_pw==user.hashed_pw:
				print ('Test worked')
				return user.id
			else:
				messages.append('Wrong password')
		except:
			messages.append('User not registered')

		if len(messages) > 0:
			return messages

class User(models.Model):
	name = models.CharField(max_length=250)
	username = models.CharField(max_length=250)
	hashed_pw = models.CharField(max_length=250)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects=UserManager()

class TripManager(models.Manager):
    def add_new(self, data, user_id):
        messages = []

        for field in data:
            if len(data[field]) == 0:
                fields = {
                    'destination': 'Destination',
                    'plan': 'Description',
                    'start_date': 'Travel Date From',
                    'end_date': 'Travel Date To'
                }
                messages.append(fields[field]+' must be filled in')

        if data['start_date'] or data['end_date']:
            start_date = datetime.datetime.strptime(data['start_date'], "%Y-%m-%d")
            end_date = datetime.datetime.strptime(data['end_date'], "%Y-%m-%d")
            now = datetime.datetime.today()

            if start_date <= now:
                messages.append('Date FROM must be in the future')

            if end_date <= now:
                messages.append('Date TO must be in the future')

            if end_date < start_date:
                messages.append('Date TO cannot be before Date FROM')

        #  Check for any overlapping of trips
        #  user = User.objects.get(id=user_id)
        # user_trips = Trip.objects.filter(planned_by__id=user.id) | Trip.objects.filter(party_people__id=user.id)
        #
        # for trip in user_trips:
        #     start_date = datetime.datetime.strptime(data['start_date'], "%Y-%m-%d")
        #     end_date = datetime.datetime.strptime(data['end_date'], "%Y-%m-%d")
        #
        #     if

        if len(messages) == 0:
            user = User.objects.get(id=user_id)
            new_trip = Trip.objects.create(planned_by=user, destination=data['destination'], start_date=data['start_date'], end_date=data['end_date'], plan=data['plan'])
            return new_trip.id
        else:
            return messages

class Trip(models.Model):
    planned_by = models.ForeignKey(User)
    party_people = models.ManyToManyField(User, related_name='trips')
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=TripManager()
