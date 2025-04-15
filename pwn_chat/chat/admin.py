from django.contrib import admin
from .models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver', 'text', 'timestamp')
    search_fields = ('sender','receiver', 'text', 'timestamp')
    list_filter = ('sender','receiver', 'text', 'timestamp')
