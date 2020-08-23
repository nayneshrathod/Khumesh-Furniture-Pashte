from django.contrib import admin

from blogs.models import post
from .models import extenduser

# Register your models here.
admin.site.register(extenduser)
admin.site.register(post)
