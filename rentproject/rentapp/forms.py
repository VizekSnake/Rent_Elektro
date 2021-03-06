from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from .models import Profile, PowerTool, RentToolProposition


# from django.db.models.signals import post_save
# from django.dispatch import receiver


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class ToolUserAddForm(forms.ModelForm):
    class Meta:
        model = PowerTool
        fields = ['brand', 'type', 'description', 'power', 'condition', 'deposit', 'price', 'tool_img']
        # widgets = {'category': forms.CheckboxSelectMultiple, }


class DateInput(forms.DateInput):
    input_type = 'date'


class RentToolPropoForm(forms.ModelForm):
    class Meta:
        model = RentToolProposition
        fields = ['from_date', 'to_date']
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
        }


class MyToolUpdateForm(forms.ModelForm):
    class Meta:
        model = PowerTool
        fields = ['price', 'description', 'power', 'type', 'condition', 'price', 'deposit','tool_img', 'category']

class SearchBarToolForm(forms.ModelForm):
    class Meta:
        model = PowerTool
        fields = ['type']
