from django.contrib import admin
from .models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'text', 'timestamp')
    search_fields = ('sender', 'text', 'timestamp')
    list_filter = ('sender', 'text', 'timestamp')
