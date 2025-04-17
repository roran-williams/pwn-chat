from .models import Project, Priority, TicketStatus, Ticket, TicketComment
from django.contrib import admin

class TicketCommentInLine(admin.TabularInline):
    model = TicketComment
    fk_name = "ticket"
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    model = Project


class PriorityAdmin(admin.ModelAdmin):
    model = Priority


class TicketStatusAdmin(admin.ModelAdmin):
    model = TicketStatus


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    inlines = [TicketCommentInLine]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Priority, PriorityAdmin)
admin.site.register(TicketStatus, TicketStatusAdmin)
admin.site.register(Ticket, TicketAdmin)
