from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from extapp.models import *


# Create your views here.
def homepage(request):
    datas = post.objects.filter(post_publish_status=True)
    return render(request, 'home.html', {'data': datas, 'title': 'HOme', 'home_active': 'active'})


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
    dataa = extenduser.objects.all()
    datas = post.objects.filter(post_writer=request.user.id)
    print(datas)

    return render(request, 'dashboard.html',
                  {'data': datas, 'dataa': dataa, 'title': 'Dashboard', 'dashboard_active': 'active', })


#
# @login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def add_post(request):
    if request.method == 'GET':
        return render(request, 'add_post.html', {'title': 'Add Post', 'add_post_active': 'active'})

    if request.method == 'POST' and request.FILES['post_file']:
        if request.POST['post_title'] and request.POST['post_description'] and request.FILES['post_file']:
            try:
                user = User.objects.get(username=request.user)
                print(user)
                post_img = request.FILES['post_file']
                fs = FileSystemStorage()
                filename = fs.save(post_img.name, post_img)
                url = fs.url(filename)
                print(url)
                # post_publish_status = request.POST.get('post_publish_status')
                # post_publish_status = True if post_publish_status else False

                if request.POST.get('post_publish_status', False):
                    post_publish_status = True
                    print(post_publish_status)
                    b = post.objects.create(post_writer=user, post_title=request.POST['post_title'],
                                            post_description=request.POST['post_description'],
                                            post_publish_status=post_publish_status,
                                            post_image=url)
                    b.save()
                else:

                    b = post.objects.create(post_writer=user, post_title=request.POST['post_title'],
                                            post_description=request.POST['post_description'],
                                            post_publish_status=False,
                                            post_image=url)
                    b.save()
                return redirect('show')
            except User.DoesNotExist:
                return render(request, 'add_post.html', {'title': 'Add Post', 'add_post_active': 'active'})
        else:
            return render(request, 'add_post.html',
                          {'erroe': 'All Data Must Be fill', 'title': 'Add Post', 'add_post_active': 'active'})
    else:
        return render(request, 'add_post.html', {'title': 'Add Post', 'add_post_active': 'active'})


def post_view(request, id):
    data = post.objects.get(id=id)
    return render(request, 'post_views.html', {'data': data, 'title': data.post_title, 'add_post_active': 'active'})


def post_delete(request, id):
    data = post.objects.get(id=id)
    return render(request, 'post_views.html', {'data': data, 'title': data.post_title, 'add_post_active': 'active'})


def post_update(request, id):
    if request.method == 'POST':  # and request.FILES['post_file']:
        data = post.objects.get(id=id)
        post_title = request.POST['post_title'] or None
        post_description = request.POST['post_description'] or None
        if request.FILES['post_file']:
            # post_img = request.FILES['post_file'] or None
            post_img = request.FILES['post_file']
            fs = FileSystemStorage()
            filename = fs.save(post_img.name, post_img)
            url = fs.url(filename)
            print(url)
            s = post.objects.filter(id=id).update(post_title=post_title,
                                                  post_description=post_description,
                                                  post_image=url)
        else:
            s = post.objects.filter(id=id).update(post_title=post_title,
                                                  post_description=post_description )
        # return render(request, 'post_views.html', {'data': data, 'title': data.post_title, 'add_post_active': 'active'})
        return redirect('home')


def post_edit(request, id):
    data = post.objects.get(id=id)
    return render(request, 'edit_post.html', {'data': data, 'title': data.post_title, 'add_post_active': 'active'})


def post_publish(request, id):
    p = post.objects.get(id=id)
    if p.post_publish_status == True:
        post.objects.filter(id=id).update(post_publish_status=False)
    else:
        post.objects.filter(id=id).update(post_publish_status=True)
    return redirect('show')
