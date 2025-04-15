from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from private_chat.models import PrivateMessage

# Create your views here.

def private_chat_room(request, username):
    other_user = get_object_or_404(User, username=username)
    
    # Get the chat history between the logged-in user and the other user
    messages = PrivateMessage.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    return render(request, 'private_chat.html', {
        'other_user': other_user,
        'messages': messages,
    })

