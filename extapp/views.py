import json
from django.views import View
from blogs.models import post
from django.urls import reverse
from django.conf import settings
from validate_email import validate_email
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from extapp.models import extenduser, feedback
from extapp.utils import account_activation_token
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError


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


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            print("Login >> True > if request.user.is_authenticated")
            return redirect("show")
        else:
            print("Login >> False > if request.user.is_authenticated")
            return render(request, 'login.html', {'title': 'Login', 'login_active': 'active'})
        # return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST,
            'title': 'Login',
            'login_active': 'active'

        }

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username + ' you are now logged in')
                    return redirect('show')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'login.html', context)
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'login.html', context)

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'login.html', context)


class RegistrationView(View):
    def get(self, request):
        # if request.method == 'GET':
        if request.user.is_authenticated:
            print("Sign up >> True > if request.user.is_authenticated")
            return redirect("show")
        else:
            print("Sign up >> False > if request.user.is_authenticated")
            return render(request, 'signup.html', {'title': 'Sign Up', 'sign_active': 'active'})

        # return render(request, 'signup.html', {'title': 'Sign Up', 'sign_active': 'active'})

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # password_confirm = request.POST['password1']
        profile_pic = request.FILES['myfile']

        context = {
            'fieldValues': request.POST,
            'title': 'Sign Up',
            'sign_active': 'active'

        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                # if password != password_confirm:
                #     messages.error(request, 'Password Not Match')
                #     return render(request, 'signup.html', context)
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'signup.html', context)

                profile = profile_pic
                fs = FileSystemStorage()
                filename = fs.save(profile.name, profile)
                url = fs.url(filename)
                user = User.objects.create_user(username=username, email=email,
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])
                user.set_password(password)
                user.is_active = False
                user.save()

                eu = extenduser.objects.create(mobileno=request.POST['mob'],
                                               age=request.POST['age'],
                                               profile_pic=url, user=user)
                eu.save()

                # user = User.objects.create_user(username=username, email=email)
                # user.set_password(password)
                # user.is_active = False
                # user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://' + current_site.domain + link

                email = EmailMessage(
                    email_subject,
                    'Hi ' + user.username + ', Please the link below to activate your account \n' + activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'signup.html', context)

        return render(request, 'signup.html', {'title': 'Sign Up', 'sign_active': 'active'})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')


'''
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
'''

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

'''
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

'''

'''


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')

'''
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
