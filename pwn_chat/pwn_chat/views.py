from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def homepage(request):
    return render(request, 'homepage.html')


def login_view(request):
    # If the user is already authenticated, redirect to the chat page
    if request.user.is_authenticated:
        return redirect('/rooms/')  # Redirect to chat if already logged in
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            
            # Check if there's a 'next' URL and redirect there, otherwise go to 'chat'
            next_url = request.GET.get('next', '/rooms/')
            return redirect(next_url)  # Redirect to the requested URL or default to 'chat'
        else:
            messages.error(request, 'Invalid username or password')  # Show error message if credentials are incorrect
            return redirect('/login/')  # Redirect back to the login page
    
    return render(request, 'login.html')  # Render login page if it's a GET request

# Logout view - Logs the user out
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('/login/')  # Redirect to login page after logging out
