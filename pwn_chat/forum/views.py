from django.shortcuts import render , redirect

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .models import Message 
from rooms.models import Room


from django.utils import timezone

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def chat_room(request,room_name):
    rooms = Room.objects.all()
    is_room = False
    
    for r in rooms:
        if r.name == room_name:
            is_room = True
    
    if is_room:
        room=Room.objects.get(name=room_name)

    else:
        room=Room.objects.create(name=room_name,created_by=request.user)
    
    
    # Get the username of the logged-in user
    username = request.user.username
    
    # Retrieve all messages ordered by timestamp in descending order (latest first)
    messages_list = Message.objects.filter(room=room).order_by('timestamp')
    last_message_timestamp = messages_list.first().timestamp if messages_list.first() else None
    message_count = messages_list.count()
   
    # Convert all timestamps to local time zone for display
    messages_with_local_time = [
    {
        'username': message.sender.username,
        'text': message.text,
        'timestamp': message.timestamp
    }
    for message in messages_list
]

    # Set up pagination: show 10 messages per page
    paginator = Paginator(messages_with_local_time, 10)  # 10 messages per page
    
    # Get the current page number from the request (default to 1)
    page_number = request.GET.get('page',-1)
    
    # Get the page object based on the page number
    page_obj = paginator.get_page(page_number)
    
    # Pass the username and the paginated messages to the template
    return render(request, "chat.html", {'message_count':message_count, 'last_message_timestamp':last_message_timestamp, 'room': room,'username': username, 'page_obj': page_obj})


