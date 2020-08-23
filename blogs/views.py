from django.shortcuts import render
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from extapp.models import extenduser
from blogs.models import post


@login_required(login_url='/accounts/login/')
def showdata(request):
    dataa = User.objects.filter(id=request.user.id)

    print(dataa)
    # datac = extenduser.objects.get(id=request.user.id)
    # print(datac)
    datas = post.objects.filter(post_writer=request.user.id)
    print(datas)

    return render(request, 'dashboard.html',
                  {'data': datas, 'd': dataa, 'title': 'Dashboard', 'dashboard_active': 'active', })


@login_required(login_url='/accounts/login/')
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
    # data = post.objects.get(id=id)
    data = post.objects.filter(id=id).delete()
    return redirect('show')
    # return render(request, 'post_views.html', {'data': data, 'title': "Data Is Deleted", 'add_post_active': 'active'})


def post_edit(request, id):
    data = post.objects.get(id=id)
    return render(request, 'edit_post.html',
                  {'data': data, 'title': 'Edit ' + data.post_title, 'add_post_active': 'active'})


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
                                                  post_description=post_description)
        # return render(request, 'post_views.html', {'data': data, 'title': data.post_title, 'add_post_active': 'active'})
        return redirect('home')


def post_publish(request, id):
    p = post.objects.get(id=id)
    if p.post_publish_status == True:
        post.objects.filter(id=id).update(post_publish_status=False)
    else:
        post.objects.filter(id=id).update(post_publish_status=True)
    return redirect('show')
