from django.contrib import admin
from .models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'timestamp')
    search_fields = ('user', 'text', 'timestamp')
    list_filter = ('user', 'text', 'timestamp')