from django.contrib import admin
from rentapp.views import home_view, SignupView, activation_sent_view, activate

from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]
