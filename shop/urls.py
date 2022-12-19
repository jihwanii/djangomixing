from django.urls import path
from .views import *

app_name = 'shop' # 이것이 있기 때문에 model에서 shop:product_detail 코드가 작성 가능해지는 것임.
urlpatterns = [
    path('', product_in_category, name='product_all'),
    path('<slug:category_slug>/', product_in_category, name='product_in_category'), # slug:category_slug의 : 뒤의 category_slug은 view의 product_in_category 함수의 파라미터에서 가져옴.
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'), # :부분을 안쓰고 이렇게 작성해도 동작은 됨. 크게 상관 없음.
    path('product_register', Product_Register.as_view(), name='product_register')
]