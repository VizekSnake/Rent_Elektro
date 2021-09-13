from django.shortcuts import render, redirect
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, ToolUserAddForm
from django.contrib import messages
from django.views import View
from .models import PowerTool, Message
from django.contrib.auth.models import User
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
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


@login_required
def Inbox(request):
    messages = Message.get_messages(user=request.user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, recipient=message['user'])
        directs.update(is_read=True)
        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    return render(request, 'inbox.html', context={
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct, })


@login_required
def UserSearch(request):
    query = request.GET.get("q")
    context = {}

    if query:
        users = User.objects.filter(Q(username__icontains=query))
        # Pagination
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        return render(request, 'search_user.html', context={
            'users': users_paginator})
    else:
        users = User.objects.all()
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
        return render(request, 'search_user.html', context={
            'users': users_paginator})

@login_required
def Directs(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)
    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    return render(request, 'inbox.html', context={
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    })


@login_required
def NewConversation(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('usersearch')
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
    return redirect('inbox')


@login_required
def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')
    else:
        HttpResponseBadRequest()


def checkDirects(request):
    directs_count = 0
    if request.user.is_authenticated:
        directs_count = Message.objects.filter(user=request.user, is_read=False).count()

    return {'directs_count': directs_count}
