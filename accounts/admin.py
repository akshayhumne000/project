from django.contrib import admin
# step 28:- import models
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin
# step 29:- create class
class CustomUserAdmin(UserAdmin): 
    list_display=['username','email','first_name','last_name','is_staff','role']
    ordering=('-date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()
admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)
