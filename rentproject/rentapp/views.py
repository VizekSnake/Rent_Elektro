from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# from .tokens import account_activation_token
from django.template.loader import render_to_string
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, ToolUserAddForm
from django.views import View
from django.contrib import messages
from rentapp.models import PowerTool


def home_view(request):
    tools = PowerTool.objects.all()
    return render(request, 'home.html', context={'tools': tools})


def profile(request):
    return render(request, 'profile.html')


def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def activation_sent_invalid(request):
    return render(request, 'activation_invalid.html')


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     # checking if the user exists, if the token is valid.
#     if user is not None and account_activation_token.check_token(user, token):
#         # if valid set active true
#         user.is_active = True
#         # set signup_confirmation true
#         user.profile.signup_confirmation = True
#         user.save()
#         login(request, user)
#         message = 'Thanks for confirming your email address!'
#         return redirect('login', context={'message': message})
#     else:
#         return render(request, 'activation_invalid.html')


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
            # current_site = get_current_site(request)
            # subject = 'Please Activate Your Account'
            # message = render_to_string('activation_request.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject, message)
            messages.success(request, f"Email with activation link has been sent to {user.username}")
            return redirect('login')
        else:
            messages.error(request, 'Username already exists')
            return redirect('signup')


class ProfileUpdateView(View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'profile_update_view.html', context={'u_form': u_form,
                                                                    'p_form': p_form})

    def post(self, request):
        ''' form to update profile info '''
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
        ''' form to add Powertool to rent '''
        tool_addform = ToolUserAddForm(request.POST)
        if tool_addform.is_valid():
            tool_addform.save()
            messages.success(request, f'Your tool has been added!')
            return redirect('profile')
