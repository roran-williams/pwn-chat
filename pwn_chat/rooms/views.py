from django.http import HttpResponseRedirect
from django.shortcuts import render 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from forum.models import Message 
from .models import Room, Status
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.
def update(request, room_name):
    
    room = get_object_or_404(Room, name=room_name)
    status_list = Status.objects.all()

    return render(request, 'update_room.html', {
        'room': room,'status_list':status_list,
    })

def update_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    name = request.POST['name']
    status = Status.objects.get(pk=int(request.POST['status']))
    description = request.POST['desc']
    room.name = name
    room.desc = description
    room.status = status
    room.update_time = timezone.now()
    room.save()

    messages.success(request, "The room has been updated.")
    return HttpResponseRedirect(f"/forum/{room.name}/")


def room_list(request):
    username = request.user.username
    rooms = Room.objects.all()
    count_list = []
    for room in rooms:
        m = Message.objects.filter(room__name=room.name).count()
        count_list.append({"name":room.name,'count':m})

    return render(request, 'room_list.html', {'count_list':count_list,'username':username,'rooms': rooms})

