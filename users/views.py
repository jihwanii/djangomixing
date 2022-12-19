from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from users.forms import *
from django.views.generic import CreateView
from django.views import View


# Create your views here.

def index_view(request):
    return render(request, 'base.html')

def singup_main(request):
    return render(request, 'registermain.html')

def login_view(request):
    return render(request, 'login.html')

class Customer_Singup_View(CreateView):
    model = NormalUser
    form_class = NormalUserForm
    template_name = 'customer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class Seller_Singup_View(CreateView):
    model = NormalUser
    form_class = SellerForm
    template_name = 'seller_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class Buyer_Singup_View(CreateView):
    model = NormalUser
    form_class = BuyerForm
    template_name = 'buyer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {"form":form}
        return render(request, "login.html", context) # 빈 form을 제공
    
    def post(self, request):
        form = LoginForm(request.POST) # 사용자의 입력값을 유지
        if form.is_valid(): # 유효성 검사 결과가 True라면
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        context = {"form":form}
        return render(request, "login.html", context)

def log_out(request):
    logout(request)
    return redirect("home")