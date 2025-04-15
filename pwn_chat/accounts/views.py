from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm
from .models import Profile
from .forms import ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            Profile.objects.create(user=user)
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def profile(request, username=None):
    # Allow viewing other users' profiles
    if username:
        user_profile = get_object_or_404(Profile, user__username=username)
    else:
        user_profile = Profile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile/', username=user_profile.user.username)
    else:
        form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'profile.html', {
        'form': form, 
        'profile': user_profile,
        })

