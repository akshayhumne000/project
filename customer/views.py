from django.shortcuts import render,get_object_or_404
from accounts.models import UserProfile,User
from django.contrib.auth.decorators import login_required
from accounts.forms import Userinfoform,userProfileForm

@login_required(login_url='login')
def cprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    #user=get_object_or_404(User,user=request.user)
    profile_form=userProfileForm(instance=profile)
    user_form=Userinfoform()
    context={
        'profile_form':profile_form,
        'user_form':user_form,
    }
    return render(request,'customer/cprofile.html',context)