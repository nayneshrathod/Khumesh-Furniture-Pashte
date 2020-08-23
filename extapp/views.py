from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from extapp.models import extenduser, feedback
from blogs.models import post
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def homepage(request):
    datas = post.objects.filter(post_publish_status=True)
    return render(request, 'home.html', {'data': datas, 'title': 'Home', 'home_active': 'active'})


# Create your views here.
def about(request):
    data = extenduser.objects.all()
    data = data[0:3]
    return render(request, 'about.html', {'data': data, 'title': 'About', 'about_active': 'active'})


def contact(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            dataa = extenduser.objects.get(user=request.user.id)
            return render(request, 'contact.html', {'d': dataa, 'title': 'Contact', 'contact_active': 'active'})
        else:
            return render(request, 'contact.html', {'title': 'Contact', 'contact_active': 'active'})
    if request.method == 'POST':
        if request.POST['email'] and request.POST['ful_name'] and request.POST['subject'] and request.POST['message']:
            fb = feedback.objects.create(fbs_email=request.POST['email'], fbs_name=request.POST['ful_name'],
                                         fbs_subject=request.POST['subject'], fbs_message=request.POST['message'])
            fb.save()
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            to_email = request.POST.get('email', '')
            from_email = settings.EMAIL_HOST_USER
            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, [to_email])
                    messages.success(request, "Mail Send Succsffully")
                    return redirect('contact')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                # return HttpResponseRedirect('contact')
                return redirect('contact')
            else:
                # In reality we'd use a form class
                # to get proper validation errors.
                messages.warning(request, "Make sure all fields are entered and valid.")
                return redirect('contact')
                # return HttpResponse('Make sure all fields are entered and valid.')
            messages.success(request, "Feedback Send")
            return redirect('contact')
        else:
            return render(request, 'contact.html', {'error': 'Plese Enter Value', 'contact_active': 'active'})


#
# def send_email(request):
#     subject = request.POST.get('subject', '')
#     message = request.POST.get('message', '')
#     from_email = request.POST.get('email', '')
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ['nayneshrathod@gmail.com'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponseRedirect('contact')
#     else:
#         # In reality we'd use a form class
#         # to get proper validation errors.
#         return HttpResponse('Make sure all fields are entered and valid.')
#

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
                user = auth.authenticate(username=request.POST['email'], password=request.POST['password'])
                if user is not None:
                    auth.login(request, user)
                    return redirect('show')
                else:
                    return render(request, 'login.html',
                                  {'error': 'Invalid  username and password', 'title': 'Login',
                                   'login_active': 'active'})
            except User.DoesNotExist:
                return render(request, 'login.html',
                              {'error': 'User Does Not Exist', 'title': 'Login', 'login_active': 'active'})
        else:
            return render(request, 'login.html', {'error': 'Plese Enter username and password', 'active': 'active'})
    # else:
    #     return render(request, 'login.html', {'error': 'Wel-Come Dear.', 'active': 'active'})


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
            if request.POST['password'] and request.POST['password1'] and request.POST['first_name'] and request.POST[
                'last_name'] and request.POST['age'] and request.POST['mob'] and request.POST['email'] and \
                    request.FILES['myfile']:
                try:
                    user = User.objects.get(username=request.POST['email'])
                    # user = User.objects.get(email=request.POST['email'])

                    return render(request, 'signup.html',
                                  {'error': 'User is Alredy exist', 'title': 'Sign Up', 'sign_active': 'active'})
                except User.DoesNotExist:
                    profile = request.FILES['myfile']
                    fs = FileSystemStorage()
                    filename = fs.save(profile.name, profile)
                    url = fs.url(filename)
                    user = User.objects.create_user(username=request.POST['email'],
                                                    email=request.POST['email'],
                                                    password=request.POST['password'],
                                                    first_name=request.POST['first_name'],
                                                    last_name=request.POST['last_name'])
                    eu = extenduser.objects.create(mobileno=request.POST['mob'],
                                                   age=request.POST['age'],
                                                   profile_pic=url,
                                                   user=user)
                    eu.save()
                    # messages.success(request, "Sign Up SuccsessFull <br>  Login Here")
                    # return redirect('login')
                    auth.login(request, user)
                    return redirect('show')
            else:
                return render(request, 'signup.html',
                              {'error': 'Empty Field', 'title': 'Sign Up', 'sign_active': 'active'})
        else:
            return render(request, 'signup.html',
                          {'error': 'Password Dose anot match', 'title': 'Sign Up', 'sign_active': 'active'})
    # else:
    #     return render(request, 'signup.html', {'title': 'Sign Up', 'sign_active': 'active'})


def logout(request):
    auth.logout(request)
    return redirect('login')

#
# def login(request):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             print("Login >> True > if request.user.is_authenticated")
#             return redirect("show")
#         else:
#             print("Login >> False > if request.user.is_authenticated")
#             return render(request, 'login.html', {'title': 'Login', 'login_active': 'active'})
#
#     if request.method == 'POST':
#         if request.POST['email'] and request.POST['password']:
#             try:
#                 # user = auth.authenticate(email=request.POST['email'])
#                 user = User.objects.get(email=request.POST['email'])
#                 auth.login(request, user)
#                 # return  redirect('home')
#                 return redirect('show')
#             except User.DoesNotExist:
#                 return render(request, 'login.html',
#                               {'error': 'User Does Not Exist', 'title': 'Login', 'login_active': 'active'})
#         else:
#             return render(request, 'login.html', {'error': 'Empty Field', 'title': 'Login', 'login_active': 'active'})
#     else:
#         return render(request, 'login.html', {'title': 'Login', 'login_active': 'active'})
