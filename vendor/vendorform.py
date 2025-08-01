from django import forms 
from .models import Vendor 
from accounts.validation import *
class vendorform(forms.ModelForm):
    vendor_license=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    class Meta:
        model=Vendor
        fields=['vendor_name','vendor_license']
    