from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import *


# Create your views here.
def homepage(request):
    return render(request, 'home.html', {'title': 'HOme', 'home_active': 'active'})


# Create your views here.
def about(request):
    return render(request, 'about.html', {'title': 'About', 'about_active': 'active'})


def contact(request):
    return render(request, 'contact.html', {'title': 'Contact', 'contact_active': 'active'})


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("Login >> True > if request.user.is_authenticated")
            return redirect("show")
        else:
            print("Login >> False > if request.user.is_authenticated")
            return render(request, 'login.html', {'title': 'Login', 'login_active': 'active'})
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password']:
            try:
                # user = auth.authenticate(email=request.POST['email'])
                user = User.objects.get(email=request.POST['email'])
                auth.login(request, user)
                # return  redirect('home')
                return redirect('show')
            except User.DoesNotExist:
                return render(request, 'login.html',
                              {'error': 'User Does Not Exist', 'title': 'Login', 'login_active': 'active'})
        else:
            return render(request, 'login.html', {'error': 'Empty Field', 'title': 'Login', 'login_active': 'active'})
    else:
        return render(request, 'login.html', {'title': 'Login', 'login_active': 'active'})


# def login(request):
#     if request.method == 'POST':
#         user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
#         if user is not None:
#             auth.login(request, user)
#             return redirect('show')
#             # return HttpResponse("Logged In")
#         else:
#             return render(request, 'login.html', {'error': 'INvalid username and password', 'active': 'active'})
#     else:
#         return render(request, 'login.html', {'error': 'Wel-Come Dear.', 'active': 'active'})


def signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("Sign up >> True > if request.user.is_authenticated")
            return redirect("show")
        else:
            print("Sign up >> False > if request.user.is_authenticated")
            return render(request, 'signup.html', {'title': 'Sign Up', 'sign_active': 'active'})

    if request.method == 'POST' and request.FILES['myfile']:
        if request.POST['password'] == request.POST['password1']:
            if request.POST['password'] and request.POST['password1'] and request.POST['username'] and request.POST[
                'first_name'] and request.POST['last_name'] and request.POST[
                'age'] and request.POST['mob'] and request.POST['email'] and request.FILES['myfile']:
                try:
                    # user = User.objects.get(username=request.POST['username'])
                    user = User.objects.get(email=request.POST['email'])

                    return render(request, 'signup.html',
                                  {'error': 'USer is Alredy exist', 'title': 'Sign Up', 'sign_active': 'active'})
                except User.DoesNotExist:
                    profile = request.FILES['myfile']
                    fs = FileSystemStorage()
                    filename = fs.save(profile.name, profile)
                    url = fs.url(filename)
                    user = User.objects.create_user(username=request.POST['username'],
                                                    email=request.POST['email'],
                                                    password=request.POST['password'],
                                                    first_name=request.POST['first_name'],
                                                    last_name=request.POST['last_name'])
                    eu = extenduser.objects.create(mobileno=request.POST['mob'],
                                                   age=request.POST['age'],
                                                   profile_pic=url,
                                                   user=user)
                    eu.save()
                    messages.success(request, "Sign Up SuccsessFull \n Login Here")
                    # auth.login(request, user)
                    return redirect('login')
            else:
                return render(request, 'signup.html',
                              {'error': 'Empty Field', 'title': 'Sign Up', 'sign_active': 'active'})
        else:
            return render(request, 'signup.html',
                          {'error': 'Password Dose anot match', 'title': 'Sign Up', 'sign_active': 'active'})
    else:
        return render(request, 'signup.html', {'title': 'Sign Up', 'sign_active': 'active'})


@login_required(login_url='/login/')
def showdata(request):
    # datas = extenduser.objects.filter(user=request.user)
    datas = extenduser.objects.all()
    return render(request, 'dashboard.html', {'data': datas, 'title': 'Dashboard', 'dashboard_active': 'active', })


#
# @login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('login')
