from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
# Create your views here.
def index(request):
	return render(request, 'login2/index.html')

def register(request): 
	postData = {
		'first_name': request.POST['first_name'],
		'last_name': request.POST['last_name'],
		'email': request.POST['email'],
		'password': request.POST['password'],
		'confirm_pw': request.POST['confirm_pw']
	}
	results = User.objects.rvalidate(postData)

	if results[0]: #there were errors
		for err in results[1]:
			print err
			messages.error(request, err) #display messages
		return redirect('/')
	else:
		request.session['logged_in_user'] = results[1].id
	return redirect('/success')

def login(request):
	postData = {
		'email': request.POST['email'],
		'password': request.POST['password']
	}

	results = User.objects.lvalidate(postData)
	
	if results == None:
		messages.error(request, "Wrong credentials")
		return redirect('/')
	elif results[0]:
		request.session['logged_in_user'] = results[1].id
		return redirect('/success')
	else:
		messages.error(request, results[1])
		return redirect('/')

def success(request):
	context = {
		'user': User.objects.get(id = request.session['logged_in_user'])
	}
	return render(request, 'login2/success.html', context)

def logout(request):
	request.session.pop('logged_in_user')
	return redirect('/')
