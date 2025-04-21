from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.models import User


class Priority(models.Model):
    name = models.CharField(max_length=32)
    value = models.IntegerField()
    is_default = models.BooleanField(default=False)
    display_color = models.TextField(max_length=16, default="#000000")

    def __str__(self):
        return f"{self.name} ({self.value})"


class TicketStatus(models.Model):
    name = models.CharField(max_length=32)
    is_default = models.BooleanField(default=False)
    hide_by_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    organization = models.CharField(max_length=28, null=True)
    name = models.CharField(max_length=28)
    desc = models.TextField()
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    status = models.ForeignKey(TicketStatus,null=True, on_delete=models.CASCADE)  # Use ForeignKey to Status

    creation_time = models.DateTimeField()
    update_time = models.DateTimeField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name='tickets_created', on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name='tickets_assigned', on_delete=models.CASCADE
    )


    def __str__(self):
        return f"{self.name} (organization: {self.organization}, Priority: {self.priority}, Assigned: {self.assigned_to})"

    class Meta:
        permissions = [
            ('can_view_status', 'Can view ticket status'),
            ('can_change_status', 'Can change ticket status'),
            ('can_assign_ticket', 'Can assign tickets'),
        ]


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    commenter = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )
    text = models.TextField()

    update_time = models.DateTimeField()

    def __str__(self):
        return f"{self.commenter} (ticket: {self.ticket.name})"
