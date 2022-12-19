from django.urls import path
from .views import *



app_name = 'users'

urlpatterns = [
    path('sing_up_main/', singup_main,name='sing_up_main'),
    path('user_sing_up/', Customer_Singup_View.as_view(),name='user_sing_up'),
    path('seller_sing_up/', Seller_Singup_View.as_view(),name='seller_sing_up'),
    path('buyer_sing_up/', Buyer_Singup_View.as_view(),name='buyer_sing_up'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', log_out,name='logout'),
]