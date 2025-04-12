from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Message, Room
from django.utils import timezone
from django.core.paginator import Paginator


def room_list(request):
    username = request.user.username
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'username':username,'rooms': rooms})

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

    # Convert all timestamps to local time zone for display
    messages_with_local_time = [
    {
        'username': message.user.username,
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
    return render(request, "chat.html", {'room_name': room_name,'username': username, 'page_obj': page_obj})



# Login view - Handles login authentication
def login_view(request):
    # If the user is already authenticated, redirect to the chat page
    if request.user.is_authenticated:
        return redirect('chat')  # Redirect to chat if already logged in
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            
            # Check if there's a 'next' URL and redirect there, otherwise go to 'chat'
            next_url = request.GET.get('next', 'chat')
            return redirect(next_url)  # Redirect to the requested URL or default to 'chat'
        else:
            messages.error(request, 'Invalid username or password')  # Show error message if credentials are incorrect
            return redirect('login')  # Redirect back to the login page
    
    return render(request, 'login.html')  # Render login page if it's a GET request

# Logout view - Logs the user out
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirect to login page after logging out
