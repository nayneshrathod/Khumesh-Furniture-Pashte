from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
import datetime
from datetime import datetime


# Create your models here.
class extenduser(models.Model):
    mobileno = models.CharField(max_length=15)
    age = models.IntegerField()
    profile_pic = models.URLField(default='/media/profile_pic.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class feedback(models.Model):
    fbs_name = models.CharField(max_length=50)
    fbs_subject = models.CharField(max_length=150)
    fbs_email = models.CharField(max_length=100)
    fbs_message = models.CharField(max_length=1000)

    def __str__(self):
        return self.fbs_name

#
#
# class post(models.Model):
#     post_writer = models.ForeignKey(User, on_delete=models.CASCADE)
#     post_title = models.CharField(max_length=100)
#     post_description = models.CharField(max_length=7000)
#     post_image = models.URLField(default='/media/post_default.jpg')
#     post_publish_status = models.BooleanField(default=False)
#     post_publish_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     post_update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
#     post_created_date = models.DateTimeField(auto_now=True, null=True, blank=True)
#
#     def __str__(self):
#         return self.post_title
#
#     class Meta:
#         ordering = ('-post_publish_date',)
#     # def save(self, *args, **kwargs):
#     #     super().save(*args, **kwargs)
#     #     if self.last_login is not None:
#     #         self.last_login = timezone.now()
#     #         return self.last_login
