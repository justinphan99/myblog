from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from blog.models import PostModel
from .models import ProfileModel
from django.contrib.auth.models import User


# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users-login')
    else:
        form = SignUpForm
    context = {
        'form': form,
    }
    return render(request, 'users/sign_up.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance = request.user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance = request.user.profilemodel)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)

def profile_for_user(request, user):
    user = User.objects.get(username=user)
    userprofile = ProfileModel.objects.get(id=user.id)
    context = {
        'userprofile': userprofile,
        'user': user,
    }
    return render(request, 'users/profile_user.html', context)