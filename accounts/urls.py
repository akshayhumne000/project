from django.urls import path,include
from . import views
 # step 44
urlpatterns=[
    path("registerUser/",views.registerUser,name='registerUser'),
    path("registerVendor/",views.registerVendor,name='registerVendor'),
    path("customerDashboard/",views.customerDashboard,name='customerDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path("myaccount/",views.myaccount,name='myaccount'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('vendor/',include('vendor.urls')),
    path('customer/',include('customer.urls')),
]