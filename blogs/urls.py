from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from extapp.views import homepage
from blogs.views import add_post, showdata, post_delete, post_edit, post_publish, post_update, post_view

urlpatterns = [

    # path('signup/', signup, name='signup'),
    # path('login/', login, name='login', ),
    # path('logout/', logout, name='logout'),

    # path('about/', about, name='about'),
    # path('contact/', contact, name='contact'),

    path('', homepage, name='home'),
    path('show/', showdata, name='show'),
    path('add_post/', add_post, name='add_post'),
    path('post_view/<int:id>/', post_view, name='post_view'),
    path('post_delete/<int:id>/', post_delete, name='post_delete'),
    path('post_edit/<int:id>/', post_edit, name='post_edit'),
    path('post_update/<int:id>/', post_update, name='post_update'),
    path('post_publish/<int:id>/', post_publish, name='post_publish'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
