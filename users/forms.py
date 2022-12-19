from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import *
from django.db import transaction



class NormalUserForm(UserCreationForm):
    mobile = forms.CharField(required=True)
    post_code = forms.CharField(required=True)
    address = forms.CharField(required=True)
    detail_address = forms.CharField(required=True)
    profile_pic = forms.FileField(required=True)
    # email = forms.EmailField()
    class Meta(UserCreationForm.Meta):
        model = NormalUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.mobile = self.cleaned_data.get('mobile')
        user.post_code = self.cleaned_data.get('post_code')
        user.address = self.cleaned_data.get('address')
        user.detail_address = self.cleaned_data.get('detail_address')
        user.profile_pic = self.cleaned_data.get('profile_pic')
        # user.email = self.cleaned_data.get('email')
        user.save()
        return user

class SellerForm(UserCreationForm):
    mobile = forms.CharField(required=True)
    post_code = forms.CharField(required=True)
    address = forms.CharField(required=True)
    detail_address = forms.CharField(required=True)
    company = forms.CharField(required=True)
    company_profile = forms.FileField(required=True)

    class Meta(UserCreationForm.Meta):
        model = NormalUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.mobile = self.cleaned_data.get('mobile')
        user.post_code = self.cleaned_data.get('post_code')
        user.address = self.cleaned_data.get('address')
        user.detail_address = self.cleaned_data.get('detail_address')
        user.save()
        seller = Seller.objects.create(user=user)
        seller.company = self.cleaned_data.get('company')
        seller.company_profile=self.cleaned_data.get('company_profile')
        seller.save()
        return user


class BuyerForm(UserCreationForm):
    mobile = forms.CharField(required=True)
    post_code = forms.CharField(required=True)
    address = forms.CharField(required=True)
    detail_address = forms.CharField(required=True)
    company = forms.CharField(required=True)
    company_profile = forms.FileField(required=True)

    class Meta(UserCreationForm.Meta):
        model = NormalUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.mobile = self.cleaned_data.get('mobile')
        user.post_code = self.cleaned_data.get('post_code')
        user.address = self.cleaned_data.get('address')
        user.detail_address = self.cleaned_data.get('detail_address')
        user.save()
        buyer = Buyer.objects.create(user=user)
        buyer.company = self.cleaned_data.get('company')
        buyer.company_profile=self.cleaned_data.get('company_profile')
        buyer.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get('username') # 유효성 검사를 진행한 username field에 값을 추출
        password = self.cleaned_data.get('password') # 유효성 검사를 진행한 password field에 값을 추출
        try:
            user = NormalUser.objects.get(username=username) # username을 기준으로 해당 Object를 가져옴
            if user.check_password(password): # 비밀번호가 서로 일치한다면 True, 아니면 False 반환 
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except NormalUser.DoesNotExist:
            self.add_error("username", forms.ValidationError("User does not exist"))