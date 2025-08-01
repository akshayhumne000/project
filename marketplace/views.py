from django.shortcuts import render,HttpResponse
from vendor.models import Vendor
from vendor.views import get_object_or_404
from django.http import JsonResponse
from menu.models import Category,FoodItem
from .context_processor import get_cart_counter,get_cart_amount
from django.db.models import Prefetch
from .models import Cart
from django.contrib.auth.decorators import login_required
def marketplace(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)[:8]
    vendors_count=vendors.count()
    context={
        'vendors':vendors,
        'vendors_count':vendors_count,
    }
    return render(request,'marketplace/listings.html',context)
def vendor_detail(request,vendor_slug):
    vendor=get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories=Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditem',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    context={
        'vendor':vendor,
        'categories':categories
    }
    return render(request,'marketplace/vendor_detail.html',context)
def search(request):
    return HttpResponse("Search page")

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            # check if the food item exists
            try:
                fooditem=FoodItem.objects.get(id=food_id) 
                #check if the user has already added that food to the cart
                try:
                    chkCart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    #increase cart quantity
                    chkCart.quantity+=1
                    chkCart.save()
                    return JsonResponse({'status':'success','message':'Increased cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amount(request)})
                except:
                    chkCart=Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'success','message':'Food item added to cart' ,'cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amount(request)})
               
                    
            except:
                 return JsonResponse({'status':'Failed','message':'This food does not exist'})
        else:       
            return JsonResponse({'status':'Failed','message':'Invalid request'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            # check if the food item exists
            try:
                fooditem=FoodItem.objects.get(id=food_id) 
                #check if the user has already added that food to the cart
                try:
                    chkCart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    #decrease_cart quantity
                    if chkCart.quantity>1:
                        chkCart.quantity-=1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity=0
                    return JsonResponse({'status':'success','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amount(request)})
                except:
                    chkCart=Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Failed','message':"We don't have item in a cart"})
               
                    
            except:
                 return JsonResponse({'status':'Failed','message':'This food does not exist'})
        else:       
            return JsonResponse({'status':'Failed','message':'Invalid request'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})

@login_required(login_url='login')
def cart(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    context={
        'cart_items':cart_items
    }
    return render(request,'marketplace/cart.html',context)
def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            try:
                #check if the cart  item exists
                cart_item=Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'success','message':'Cart item has been deleted','cart_counter':get_cart_counter(request)})
            except:
                return JsonResponse({'status':'Failed','message':'Cart item does not exist'})
                    
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})

