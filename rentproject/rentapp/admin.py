from django.contrib import admin

# Register your models here.

from .models import Profile, Brand, PowerTool, RentToolProposition, User, Category

admin.site.register(Profile)
admin.site.register(Brand)
admin.site.register(PowerTool)
admin.site.register(Category)
admin.site.register(RentToolProposition)
