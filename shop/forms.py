'''
12.19 error product save 안됨
'''
from django import forms

from django.db import transaction
from shop.models import *

class ProductForm(forms.ModelForm): # modelform으로 받아야함
    name = forms.CharField(required=True)
    slug = forms.SlugField(required=True)
    image = forms.FileField(required=True)
    description = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    price = forms.DecimalField(required=True)
    stock = forms.CharField(required=True)
    available_display = forms.BooleanField(required=True)
    available_order = forms.BooleanField(required=True)

    class Meta():
        model = Product
        fields = '__all__'

    @transaction.atomic
    def save(self):
        product = Product.objects.get(pk=self.cleaned_data['pk'])
        product.name = self.cleaned_data.get('name')
        product.slug = self.cleaned_data.get('slug')
        product.image = self.cleaned_data.get('image')
        product.description = self.cleaned_data.get('description')
        product.meta_description = self.cleaned_data.get('meta_description')
        product.price = self.cleaned_data.get('price')
        product.stock = self.cleaned_data.get('stock')
        product.available_display = self.cleaned_data.get('available_display')
        product.available_order = self.cleaned_data.get('available_order')
        product.save()

        return product