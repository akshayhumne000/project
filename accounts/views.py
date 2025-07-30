
from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.vendorform import vendorform
from .utils import *
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required,user_passes_test
from django.template.defaultfilters import slugify
#Restrict the vendor from accessing the customer
def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

#Restrict the customer from accessing the vendor
def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied
def registerUser(request):
    if(request.method=='POST'):
        fm=UserForm(request.POST)
        if fm.is_valid():
            password=fm.cleaned_data['password']
            user=fm.save(commit=False)
            user.set_password(password)
            user.role=User.CUSTOMER
            user.save()
            #send verification email
            email_subject='Please activate your account'
            email_template='accounts/emails/account_verification_email.html'
            send_verification_email(request,user,email_subject,email_template)
            messages.success(request,"Your account has been registered successfully")
            return redirect('registerUser')
    else:
        fm=UserForm()
    context={
        'form':fm
    }
    return render(request,'accounts/registerUser.html',context)

def registerVendor(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        v_form=vendorform(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            vendor_name=v_form.changed_data['vendor_name']
            vendor.vendor_slug=slugify(vendor)+'-'+str(user.id)
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,"Your account has been registered successfully, Please wait for approval !")
            return redirect('registerVendor')
        else:
            print("Invalid Form")
            print(form.errors)
    else:
        form=UserForm()
        v_form=vendorform()
    context={
         'form':form,
         'v_form':v_form     
        }

    return render(request,'accounts/registerVendor.html',context)


@login_required
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')
@login_required
def customerDashboard(request):
    return render(request,'accounts/customerDashboard.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"you are Logged In")
            return redirect('myaccount')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request,"you are Logged Out ")
    return redirect('login')
def myaccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

def activate(request,uidb64,token):
    #activate  the user by settings the is_active status to True
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulations Your account is activated")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('myaccount')


