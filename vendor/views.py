from django.shortcuts import render,get_object_or_404,redirect
from accounts.forms import userProfileForm
from  .vendorform import vendorform
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from menu.models import Category,FoodItem
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.menuform import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify
def get_vendor(request):
    vendor=Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor=get_object_or_404(Vendor,user=request.user)
    if request.method=='POST':
        profile_form=userProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=vendorform(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,"Settings Updated")
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)

    else:
        profile_form=userProfileForm(instance=profile)
        vendor_form=vendorform(instance=vendor)

    
    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/vprofile.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor)
    context={
        'categories':categories
        
    }
    return render(request,'vendor/menu_builder.html',context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor=get_vendor(request)
    category=get_object_or_404(Category,pk=pk)
    fooditem=FoodItem.objects.filter(vendor=vendor,category=category)
    context={
        'fooditem':fooditem,
        'category':category,
    }
    return render(request,'vendor/fooditems_by_category.html',context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            form.save()
            messages.success(request,"category Added Successfully")
            return redirect("menu_builder")
        else:
            print(form.errors)
    else:
        form=CategoryForm()
    context={
        'form':form
    }
    return render(request,'vendor/add_category.html',context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            foodtitle=form.cleaned_data['food_title']
            food=form.save(commit=False)
            food.vendor=get_vendor(request)
            food.slug=slugify(foodtitle)
            form.save()
            messages.success(request,"Food Added Successfully")
            return redirect("fooditems_by_category",food.category.id)
        else:
            print(form.errors)
    else:
        form=FoodItemForm()
        #modify this form
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form
    }
    return render(request,'vendor/add_food.html',context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
             category_name=form.cleaned_data['category_name']
             category=form.save(commit=False)
             category.vendor=get_vendor(request)
             category.slug=slugify(category_name)
             form.save()
             messages.success(request,"category updated Successfully")
             return redirect("menu_builder")
        else:
            print(form.errors)
    else:
        form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category
    }
    return render(request,'vendor/edit_category.html',context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
             foodtitle=form.cleaned_data['food_title']
             food=form.save(commit=False)
             food.vendor=get_vendor(request)
             food.slug=slugify(foodtitle)
             form.save()
             messages.success(request,"Food updated Successfully")
             return redirect("fooditems_by_category",food.category.id)
        else:
            print(form.errors)
    else:
        form=FoodItemForm(instance=food)
        #modify this form
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={
        'form':form,
        'food':food
    }
    return render(request,'vendor/edit_food.html',context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk) 
    category.delete()   
    messages.success(request,"Category Deleted Successfully")
    return redirect("menu_builder")
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request,pk=None):
    category=get_object_or_404(FoodItem,pk=pk) 
    category.delete()   
    messages.success(request,"Food Item has Deleted Successfully")
    return redirect("menu_builder")

        

    
