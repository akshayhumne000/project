from django.urls import path
from accounts import views as Accountview
from . import views
urlpatterns=[
    path('',Accountview.customerDashboard,name='customer'),
    path('profile/',views.cprofile,name='cprofile'),
]