# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Trip
from django.db.models import Q
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    # User.objects.all().delete()
    # Trip.objects.all().delete()
    if 'user' in request.session:
        return render(request, 'belt_app/travels.html')
    else:
        return render(request, 'belt_app/index.html')


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
			return redirect(reverse('travels'))
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
			return redirect(reverse('travels'))
	else:
		return redirect('/')

def travels(request):
    if 'user' in request.session:
        user = User.objects.get(id=request.session['user'])
        trips = Trip.objects.filter(Q(party_people__id=user.id) | Q(planned_by__id=user.id)).order_by('start_date')
        other_trips = Trip.objects.exclude(party_people__id=user.id).exclude(planned_by__id=user.id).order_by('start_date')
        context = {
            'user': user,
            'trips': trips,
            'other_trips': other_trips
        }
        return render(request, 'belt_app/travels.html', context)
    else:
        messages.error(request, 'Log in or register first')
        return redirect('/')

def join_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user'])
    jointrip = trip.party_people.add(user)
    return redirect(reverse('travels'))

def destination(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    party_people = User.objects.filter(trips=trip)
    context = {
        'trip': trip,
        'party_people': party_people
    }
    return render(request, 'belt_app/destination.html', context)

def add(request):
    return render(request, 'belt_app/add.html')

def add_new(request):
    post_data = request.POST.copy()
    result = Trip.objects.add_new(post_data, request.session['user'])
    if isinstance(result, list):
        for err in result:
            messages.error(request, err)
        return redirect(reverse('add'))
    else:
        return redirect(reverse('travels'))

def logout(request):
	request.session.pop('user')
	return redirect('/')
