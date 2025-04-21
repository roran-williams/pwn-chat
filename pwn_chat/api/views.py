from django.shortcuts import render
from django.http import JsonResponse
from rooms.models import Room, Status
from forum.models import Message
from private_chat.models import PrivateMessage
from accounts.models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def rooms(request):
    rooms = Room.objects.all()
    data = []
    for r in rooms:
        data.append(
        {
        "room_name":r.name,
        "created_by":str(r.created_by),
        "creation_date":r.creation_time,
        "update_date":r.update_time,
        "description":r.desc,
        "status":str(r.status),
        "updated":r.update_time,
        })
    
    return JsonResponse(data,safe=False)

@login_required
def messages(request):
    messages = Message.objects.all()
    data = []
    for m in messages:
        data.append(
        {
         'forum':str(m.room),
         "data": {
                "sender":str(m.sender),
                "text":m.text,
                "timestamp":m.timestamp,
            }
         }
    )
    
    return JsonResponse(data,safe=False)

@login_required
def private_messages(request):
    messages = PrivateMessage.objects.all()
    data = []
    for m in messages:
        data.append(
         {
            "sender":str(m.sender),
            "receiver":str(m.receiver),
            "text":m.text,
            "timestamp":m.timestamp,
            }
    )
    
    return JsonResponse(data,safe=False)

@login_required
def profiles(request):
    profiles = Profile.objects.all()
    data = []
    for p in profiles:
        data.append(
         
        {
         "user":p.user.username,
         "data":{
            'first_name':p.user.first_name,
            'last_name':p.user.last_name,
            'email':p.user.email,
            'profile_picture':p.profile_picture.url,
            'created_at':p.created_at,
            'last_login':p.user.last_login,
            'status':p.status,
            'bio':p.bio,
            }
            }
            
    )
    
    return JsonResponse(data,safe=False)

@login_required
def statuses(request):
    statuses = Status.objects.all()
    data = []
    for s in statuses:
        data.append(
         {
             "status":s.name
         }
            
    )
    
    return JsonResponse(data,safe=False)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You are authenticated!', 'user': str(request.user)})
