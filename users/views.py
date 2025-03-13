from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth import login
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required

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
                authenticated_user = auth.authenticate(
                    username=user.email,
                    password=form.cleaned_data['password1']
                )
                if authenticated_user:
                    auth.login(request, authenticated_user)
                    return HttpResponseRedirect(reverse('xaki'))
                else:
                    return render(request, 'users/registration.html',
                        {'form': form, 'error': 'Ошибка при входе в аккаунт'})
            except IntegrityError:
                return render(request, 'users/registration.html',
                    {'form': form, 'error': 'Пользователь с такой почтой уже существует'})
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})

@login_required
def profile(request):
    context = {
        'user': request.user,
        'title': 'Profile'
    }
    return render(request, 'users/profile.html', context)

@login_required
def editprofile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Обработка полного имени
            full_name = form.cleaned_data.get('full_name')
            if full_name:
                name_parts = full_name.split()
                if len(name_parts) >= 2:
                    user.first_name = name_parts[0]
                    user.last_name = ' '.join(name_parts[1:])
            
            # Обработка остальных полей
            user.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.phone_number = form.cleaned_data.get('phone_number', '')
            user.gender = form.cleaned_data.get('gender', '')
            user.technology_stack = form.cleaned_data.get('technology_stack', '')
            user.group = form.cleaned_data.get('group', '')
            user.course = form.cleaned_data.get('course')
            user.student_number = form.cleaned_data.get('student_number', '')
            
            # Обработка фото
            if 'profile_photo' in request.FILES:
                user.profile_photo = request.FILES['profile_photo']
            
            user.save()
            return redirect('users:profile')
    else:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'date_of_birth': request.user.date_of_birth,
            'phone_number': request.user.phone_number,
            'gender': request.user.gender,
            'technology_stack': request.user.technology_stack,
            'group': request.user.group,
            'course': request.user.course,
            'student_number': request.user.student_number,
        }
        form = UserProfileForm(instance=request.user, initial=initial_data)
    
    return render(request, 'users/editprofile.html', {'form': form})

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