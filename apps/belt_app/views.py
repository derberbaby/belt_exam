# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
# from django.db.models import Q
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	if 'user' in request.session:
		return render(request, 'belt_app/home.html')
	else:
		return render(request, 'belt_app/index.html')

def home(request):
    return render(request, 'belt_app/home.html')

def login(request):
	if request.method=='POST': # used to prevent user from directly accessing this page (ex: localhost:8000/login)
		result = User.objects.login(request.POST.copy()) # access method, "login," in model
		if isinstance(result, list):
			for err in result:
				messages.error(request, err)
			return redirect('/')
		else:
			request.session['user'] = result
			messages.success(request, 'Successfully logged in!')
			return redirect(reverse('home'))
	else:
		return redirect('/')

def register(request):
	if request.method=='POST':
		result = User.objects.register(request.POST.copy())
		if isinstance(result, list):
			for err in result:
				messages.error(request, err)
			return redirect('/')
		else:
			request.session['user'] = result
			messages.success(request, 'Successfully registered!')
			return redirect(reverse('home'))
	else:
		return redirect('/')

def logout(request):
	request.session.pop('user')
	return redirect('/')
