from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from itertools import chain
import random

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(fullname=fullname).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            else:
                user = User.object.create_user(fullname=fullname, email=email, password1=password1)
                user.save()
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'SignUp.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST[username]
        password = request.POST[password]

        user = auth.authenticate(request, 'Credentials Invalid')

        if user is not None:
            auth.login(request, user)
            return redirect('index.html')
        else:
            messages.info('signin')

    else:
        return render(request, 'LogIn.html')
    
@login_required(login_url='signin')   
def logout(request):

    auth.logout(request)
    return redirect('signin')
    
@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
