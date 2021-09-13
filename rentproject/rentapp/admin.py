from django.contrib import admin

# Register your models here.

from .models import Profile, Brand, PowerTool

admin.site.register(Profile)
admin.site.register(Brand)
admin.site.register(PowerTool)
