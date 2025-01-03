from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender_admin', 'sender_employee', 'receiver_admin', 'receiver_employee', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('message',)
