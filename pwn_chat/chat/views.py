from django.shortcuts import render

def chat_view(request):
    username = request.user.username
    return render(request, "chat.html",{'username':username})
