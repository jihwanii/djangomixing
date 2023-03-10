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
        username = self.cleaned_data.get('username') # ????????? ????????? ????????? username field??? ?????? ??????
        password = self.cleaned_data.get('password') # ????????? ????????? ????????? password field??? ?????? ??????
        try:
            user = NormalUser.objects.get(username=username) # username??? ???????????? ?????? Object??? ?????????
            if user.check_password(password): # ??????????????? ?????? ??????????????? True, ????????? False ?????? 
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except NormalUser.DoesNotExist:
            self.add_error("username", forms.ValidationError("User does not exist"))