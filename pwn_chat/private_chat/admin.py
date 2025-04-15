from django.contrib import admin

from private_chat.models import PrivateMessage

# Register your models here.
@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver', 'text', 'timestamp')
    search_fields =  ('sender','receiver', 'text', 'timestamp')
    list_filter = ('sender','receiver', 'text', 'timestamp')
