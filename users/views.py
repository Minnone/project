from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import login
from users.forms import UserLoginForm, UserRegistrationForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('xaki'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user) # Автоматический логин после регистрации.  Можно убрать, если нужно.
                return redirect('your_redirect_url') # Замените на нужный URL
            except IntegrityError:
                      return render(request, 'users/registration.html',
                      {'form': form, 'error': 'Пользователь с таким именем уже существует'})
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})




def profile(request):
    context = {'title': 'Profile'}
    return render(request, 'users/profile.html', context)

def editprofile(request):
    context = {'title': 'Profile'}
    return render(request, 'users/editprofile.html', context)

def changelogin(request):
    context = {'title': 'Profile'}
    return render(request, 'users/changelogin.html', context)

def addmail(request):
    context = {'title': 'Profile'}
    return render(request, 'users/addmail.html', context)

def addmailcorrect(request):
    context = {'title': 'Profile'}
    return render(request, 'users/addmailcorrect.html', context)

def restorepassword(request):
    context = {'title': 'Profile'}
    return render(request, 'users/restorepassword.html', context)