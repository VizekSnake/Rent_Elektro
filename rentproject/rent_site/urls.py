"""rent_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path
from rentapp.views import home_view, SignupView, profile, ProfileUpdateView, ToolUserAddView, Inbox, \
    Directs, NewConversation, SendDirect, UserSearch, my_tools_view, ToolDetailView, RentPropositionView, RequestsView, \
    DeleteRequestView, ApproveRequestView, LendedView, RentedView, MyToolUpdateView, MyRequestsView, RejectRequestView, \
    CancelRequestView, OwnerToolReturnView, UserToolReturnView, HideView, SearchToolView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('', home_view, name="home"),
    path('profile/my_tools', my_tools_view, name="my_tools"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),
    path('change-password/',
         auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='/'),
         name='change_password'),
    path('profile/', profile, name='profile'),
    path('profile/settings', login_required(ProfileUpdateView.as_view()),
         name='profile_update'),
    path('profile/add_tool/', login_required(ToolUserAddView.as_view()), name='add_user_tool'),
    path('inbox/', Inbox, name='inbox'),
    path('directs/<username>', Directs, name='directs'),
    path('new/', UserSearch, name='usersearch'),
    path('new/<username>', NewConversation, name='newconversation'),
    path('send/', SendDirect, name='send_direct'),
    path('tool_detail/<int:tool_id>', login_required(ToolDetailView.as_view()), name='tool_detail'),
    path('rent_this_elektro/<int:elektro_id>', login_required(RentPropositionView.as_view()), name='rent_this_elektro'),
    path('profile/requests', RequestsView.as_view(), name='requests'),
    path('profile/my_requests', login_required(MyRequestsView.as_view()), name='my_requests'),
    path('reject/<int:req_id>', login_required(RejectRequestView.as_view()), name='reject'),
    path('cancel/<int:req_id>', login_required(CancelRequestView.as_view()), name='reject'),
    path('approve/<int:req_id>', login_required(ApproveRequestView.as_view()), name='approve'),
    path('profile/my_tool/update/<int:my_tool_id>', login_required(MyToolUpdateView.as_view()), name='tool_update'),
    path('profile/lended/', login_required(LendedView.as_view()), name='lended'),
    path('profile/rented/', login_required(RentedView.as_view()), name='rented'),
    path('ownertoolreturn/<int:req_id>', login_required(OwnerToolReturnView.as_view()), name='owner_tool_return'),
    path('usertoolreturn/<int:req_id>', login_required(UserToolReturnView.as_view()), name='user_tool_return'),
    path('hide/<int:req_id>', login_required(HideView.as_view()), name='hide'),
    path('search/tool', login_required(SearchToolView.as_view()), name='search')
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
