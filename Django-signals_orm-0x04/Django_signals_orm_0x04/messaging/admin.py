from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Message, Notification

admin.site.register(Message)
admin.site.register(Notification)
