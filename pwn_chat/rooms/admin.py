from django.contrib import admin

from .models import Room, Status

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'status','creation_time','update_time','created_by')
    search_fields =  ('name', 'desc', 'status','creation_time','update_time','created_by')
    list_filter = ('name', 'desc', 'status','creation_time','update_time','created_by')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'hide_by_default')
    search_fields =  ('name', 'is_default', 'hide_by_default')
    list_filter = ('name', 'is_default', 'hide_by_default')
