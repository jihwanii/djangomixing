from django import forms
from .models import Order

# form은 유효성 검사를 하기위하여 사용함.

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address',
                  'postal_code','city']