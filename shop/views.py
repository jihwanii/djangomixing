'''
12.19 error product save 안됨
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from .models import *
from .forms import *
from cart.forms import AddProductForm
from django.contrib import messages

# Create your views here.
def product_in_category(request, category_slug=None): # pageing 작업 추가하기!!!
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True) # 표시 가능한 애들만 불러오겠다.
    
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug) # Category model에서 slug가 category_slug인 애들만 불러올꺼야 아닐 시 404로 보내~
        products = products.filter(category=current_category) # 쿼리는 매번 실행되는 것이 아니라 데이터를 필요로 하는 때에만 실행되기 때문에 속도에 영향을 크게 미치지 않는다 그렇게에 마음껏 사용해도 됨.

    return render(request, 'shop/list.html', {
        'current_category':current_category,
        'categories':categories,
        'products':products
    })

def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity':1})
    return render(request, 'shop/detail.html', {'product':product, 'add_to_cart':add_to_cart})

class Product_Register(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_register.html'

    @transaction.atomic
    def form_valid(self):
        self.save()

        return redirect('product_register')

