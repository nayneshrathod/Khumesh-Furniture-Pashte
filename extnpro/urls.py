from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from extapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login',),
    path('show/', showdata, name='show'),
    path('logout/', logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
