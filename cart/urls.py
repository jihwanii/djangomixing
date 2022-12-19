from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', detail, name='detail'),
    # 아래 두 코드는 같은 기능이나 방법이 두가지여서 각각 사용함.
    path('add/<int:product_id>/', add, name='product_add'),
    path('remove/<product_id>/', remove, name='product_remove'),
]