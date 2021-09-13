from django.shortcuts import render, redirect
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, ToolUserAddForm
from django.views import View
from django.contrib import messages
from .models import PowerTool
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site


# Create your models here.

def home_view(request):
    tools = PowerTool.objects.all()
    return render(request, 'home.html', context={'tools': tools})


def profile(request):
    return render(request, 'profile.html')


class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = True
            user.save()
            messages.success(request, f'Your account has been created! {user.username} are now able to log in')
            return redirect('login')


class ProfileUpdateView(View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'profile_update_view.html', context={'u_form': u_form,
                                                                    'p_form': p_form})

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')


class ToolUserAddView(View):
    def get(self, request):
        tool_addform = ToolUserAddForm(request.POST)
        return render(request, 'add_user_tool.html', context={'tool_addform': tool_addform})

    def post(self, request):
        user = request.user
        tool_addform = ToolUserAddForm(request.POST, initial={'owner': user.id})
        if tool_addform.is_valid():
            tool = tool_addform.save(commit=False)
            tool.owner = request.user
            tool.save()
            messages.success(request, f'Your tool has been added!')
            return redirect('profile')
