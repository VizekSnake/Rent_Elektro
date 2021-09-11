from django.contrib import admin
from rentapp.views import home_view, SignupView, profile, ProfileUpdateView, activation_sent_view, \
    activation_sent_invalid, ToolUserAddView
# activate
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('', home_view, name="home"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('sent/invalid', activation_sent_invalid, name="activation_invalid"),
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
    path('profile/settings', ProfileUpdateView.as_view(),
         name='profile_update'),
    path('profile/add_tool', ToolUserAddView.as_view(), name='add_user_tool')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
