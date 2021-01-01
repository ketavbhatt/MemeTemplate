# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render,redirect
from django.http import HttpResponse
import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout


from django.http import JsonResponse
import requests
from datetime import datetime
import pytz



# Create your views here.


def login_site(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		print("asdasd")
		print(username)
		print(password)
		print(user)
		if user:
			print("asas")
			login(request, user)
			response = redirect('/cookie/')
			response.set_cookie('username', username)
			IST = pytz.timezone('Asia/Kolkata')
			response.set_cookie('last-login', datetime.now(IST))
			return response
		else:
			return HttpResponse('Invalid User')
	else:	
		return render(request, 'login.html')

def cookie(request):
	if request.method == 'POST':
		if request.user.is_authenticated():
			print(request.POST.get('login-submit'))
			if 'Accept' in request.POST.get('login-submit'):
				return redirect('/memes/')
			else :
				return redirect('/login/')
		else:
			return HttpResponse('Invalid User')
	else:	
		return render(request, 'index.html', {"username":request.COOKIES['username'] , "lastLogin":request.COOKIES['last-login'],"sessionId":request.COOKIES['sessionid']})

def memes(request):
	if request.user.is_authenticated():
		print(request.COOKIES['username'])
		result = requests.get("https://api.imgflip.com/get_memes")
		memes = result.json().get('data').get('memes')
		firstFiveMemes = memes[:5]
		print(len(firstFiveMemes))
		return render(request,'memes.html',{"memes":firstFiveMemes})
	else:
		return HttpResponse('Invalid User')



