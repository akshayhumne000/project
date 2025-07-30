from django.shortcuts import render # step 7 = create views.py  import library
from vendor.models import Vendor
def home(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)[:8] # step 9 create class 
    context={
        'vendors':vendors
    }
    return render(request,'home.html',context)