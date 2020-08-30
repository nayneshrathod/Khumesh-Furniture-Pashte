from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from extapp.views import homepage, LoginView, RegistrationView, VerificationView, UsernameValidationView, logout, \
    EmailValidationView

# , LogoutView
urlpatterns = [
    path('', homepage, name='home'),

    # path('signup/', signup, name='signup'),
    path('signup/', RegistrationView.as_view(), name='signup'),

    # path('login/', login, name='login', ),
    path('login/', LoginView.as_view(), name='login', ),

    path('logout/', logout, name='logout'),
    # path('logout/', LogoutView.as_view(), name="logout"),

    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
