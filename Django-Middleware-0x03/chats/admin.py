from django.contrib import admin
from .models import Conversation, ConversationAdmin, Message,Conversation,MessageAdmin


# Register your models here.
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)