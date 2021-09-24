from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, ToolUserAddForm, RentToolPropoForm, MyToolUpdateForm, \
    SearchBarToolForm
from django.contrib import messages
from django.views import View
from .models import PowerTool, Message, RentToolProposition
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
    user = request.user
    user_id = user.id
    requests = RentToolProposition.objects.filter(rented=False, tool__owner_id=user_id,
                                                  reservation_to_acceptation=True, isread=False)
    requests = requests.count()
    if requests > 0:
        messages.success(request, f'You have got {requests} new requests')
    return render(request, 'home.html', context={'tools': tools, 'requests': requests})

@login_required
def my_tools_view(request):
    tools = PowerTool.objects.filter(owner=request.user)
    return render(request, 'my_tools.html', context={'tools': tools})


class ToolDetailView(View):
    def get(self, request, tool_id):
        tool = PowerTool.objects.filter(id=tool_id)
        return render(request, 'tool_detail.html', context={'tool': tool})

@login_required
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


class RentalView(View):
    def get(self, request):
        return render(request, 'rental_elektro.html')

    # def post(self, request):
    #     return


class RentPropositionView(View):
    def get(self, request, elektro_id):
        detail_of_tool = PowerTool.objects.filter(id=elektro_id)
        rent_propo_form = RentToolPropoForm(request.POST)
        return render(request, 'rent_this_elektro.html',
                      context={'rent_propo_form': rent_propo_form, 'detail_of_tool': detail_of_tool})

    def post(self, request, *args, **kwargs):
        rentform = RentToolPropoForm(request.POST)
        tool_id = request.POST.get('elektro_id')
        if rentform.is_valid():
            rentform = rentform.save(commit=False)
            rentform.by_user = request.user.profile
            rentform.reservation_to_acceptation = True
            rentform.tool = PowerTool.objects.get(pk=tool_id)
            start_date = datetime.strptime(str(rentform.from_date), "%Y-%m-%d")
            today = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
            days_of_rent = (start_date - today).days
            if days_of_rent < 0:
                messages.warning(request,
                                 f'Request has not been sent! Dates are incorrect! You cant rent in past time!')
                return redirect(f'/rent_this_elektro/{tool_id}')
            if rentform.tool.owner_id == request.user.id:
                messages.warning(request, f'Request has not been sent! Its Your tool!')
                return redirect('home')
            else:
                rentform.save()
            messages.success(request, f'Request has been sent!')
            return redirect('home')


class RequestsView(View):
    def get(self, request):
        user = request.user
        user_id = user.id
        requests = RentToolProposition.objects.filter(rented=False, tool__owner_id=user_id,
                                                      reservation_to_acceptation=True, tool_owner_view=True)
        rent_price = 0
        days_of_rent = 0
        for request_tool in requests:
            request_tool.isread = True
            start_date = datetime.strptime(str(request_tool.from_date), "%Y-%m-%d")
            end_date = datetime.strptime(str(request_tool.to_date), "%Y-%m-%d")
            if request_tool.rent_price is None:
                days_of_rent = abs(end_date - start_date).days
                if days_of_rent == 0:
                    request_tool.rent_price = 1 * request_tool.tool.price
                elif days_of_rent > 0:
                    request_tool.rent_price = abs(end_date - start_date).days * request_tool.tool.price
                request_tool.save()
            else:
                days_of_rent = (end_date - start_date).days
                if days_of_rent == 0:
                    request_tool.rent_price = 1 * request_tool.tool.price
                elif days_of_rent > 0:
                    request_tool.rent_price = abs(end_date - start_date).days * request_tool.tool.price
                request_tool.save()
        return render(request, 'requests.html', context={'requests': requests, 'days_of_rent': days_of_rent})


class MyRequestsView(View):
    def get(self, request):
        user = request.user
        user_id = user.id
        requests = RentToolProposition.objects.filter(rented=False, by_user=user_id,
                                                      reservation_to_acceptation=True, by_user_view=True)
        rent_price = 0
        days_of_rent = 0
        for request_tool in requests:
            start_date = datetime.strptime(str(request_tool.from_date), "%Y-%m-%d")
            end_date = datetime.strptime(str(request_tool.to_date), "%Y-%m-%d")
            days_of_rent = (end_date - start_date).days
            if days_of_rent == 0:
                request_tool.rent_price = 1 * request_tool.tool.price
            elif days_of_rent > 0:
                request_tool.rent_price = abs(end_date - start_date).days * request_tool.tool.price
            request_tool.save()
        return render(request, 'my_requests.html', context={'requests': requests})


class LendedView(View):
    def get(self, request):
        user = request.user
        user_id = user.id
        requests = RentToolProposition.objects.filter(reservation_to_acceptation=False,
                                                      tool__owner_id=user_id)
        return render(request, 'lended.html', context={'requests': requests})


class DeleteRequestView(View):
    def get(self, request, req_id):
        request_to_delete = RentToolProposition.objects.get(pk=req_id)
        request_to_delete.delete()
        messages.warning(request, f'Request has been rejected!')
        return redirect('requests')


class RejectRequestView(View):
    def get(self, request, req_id):
        request_to_reject = RentToolProposition.objects.get(pk=req_id)
        request_to_reject.rejected = True
        request_to_reject.tool_owner_view = False
        request_to_reject.save()
        messages.warning(request, f'Request has been rejected!')
        return redirect('requests')


class HideView(View):
    def get(self, request, req_id):
        request_to_reject = RentToolProposition.objects.get(pk=req_id)
        request_to_reject.rejected = True
        request_to_reject.user_owner_view = False
        request_to_reject.save()
        messages.warning(request, f'Request has been dismiss!')
        return redirect('requests')


class CancelRequestView(View):
    def get(self, request, req_id):
        request_to_cancel = RentToolProposition.objects.get(pk=req_id)
        request_to_cancel.canceled = True
        request_to_cancel.by_user_view = False
        request_to_cancel.save()
        messages.warning(request, f'Request has been canceled!')
        return redirect('my_requests')


class ApproveRequestView(View):
    def get(self, request, req_id):
        request_to_update = RentToolProposition.objects.get(pk=req_id)
        request_to_update.reservation_to_acceptation = False
        request_to_update.accepted_by_owner = True
        request_to_update.rented = True
        request_to_update.save()
        messages.success(request, f'Request has been approved!')
        return redirect('requests')


class RentedView(View):
    def get(self, request):
        user = request.user.profile
        user_id = user.id
        requests = RentToolProposition.objects.filter(by_user=user_id)
        return render(request, 'rented.html', context={'requests': requests, 'user_id': user_id})


class UserToolReturnView(View):
    def get(self, request, req_id):
        request_return_tool = RentToolProposition.objects.get(pk=req_id)
        request_return_tool.by_user_return = True
        request_return_tool.save()
        return redirect('rented')


class OwnerToolReturnView(View):
    def get(self, request, req_id):
        request_return_tool = RentToolProposition.objects.get(pk=req_id, tool_owner_view=True)
        request_return_tool.tool_owner_return = True
        request_return_tool.rented = False
        request_return_tool.save()
        messages.success(request, f'Tool has been returned!')
        return redirect('lended')


class MyToolUpdateView(View):
    def get(self, request, my_tool_id):
        my_tool_view = PowerTool.objects.get(pk=my_tool_id)
        my_tool = get_object_or_404(PowerTool, id=my_tool_id)
        my_tool_form = MyToolUpdateForm(instance=my_tool)
        return render(request, 'my_tool_update_view.html',
                      context={'my_tool_form': my_tool_form, 'my_tool_view': my_tool_view})

    def post(self, request, *args, **kwargs):
        my_tool_id = request.POST.get('my_tool_id')
        my_tool = get_object_or_404(PowerTool, id=my_tool_id)
        my_tool_form = MyToolUpdateForm(request.POST, request.FILES, instance=my_tool)
        if my_tool_form.is_valid():
            my_tool_form.save()
            messages.success(request, f'Your tool has been updated!')
            return redirect('/profile/my_tools')


class SearchToolView(View):
    def get(self, request):
        search_form = SearchBarToolForm(request.POST)
        return render(request, 'search_tool.html', context={'search_form': search_form})

    def post(self, request):
        search_form = SearchBarToolForm(request.POST)
        if search_form.is_valid():
            searched = search_form.cleaned_data['type']
            filtrated_tools = PowerTool.objects.filter(type=searched)
        return render(request, 'search_tool.html',
                      context={"search_form": search_form, 'filtrated_tools': filtrated_tools})
