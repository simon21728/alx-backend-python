from django.contrib import admin

# Register your models here.
from .models import Message, Notification

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'content', 'read', 'timestamp')
    list_filter = ('read', 'timestamp')
    search_fields = ('user__username', 'content')

# Register the models in the admin site
admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)
