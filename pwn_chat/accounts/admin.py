from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at','status','bio')
    search_fields = ('user__username','created_at','status','bio')
    list_filter = ('user', 'created_at','status','bio')
