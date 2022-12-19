from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class NormalUser(AbstractUser):
    mobile = models.CharField(max_length=20, null=True)
    post_code = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=40, null=True)
    detail_address = models.CharField(max_length=100, null=True)
    profile_pic = models.FileField(upload_to='media/', null=True, blank=True)

class Seller(models.Model):
    user = models.OneToOneField(NormalUser, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=20, null=True)
    company_profile = models.FileField(upload_to='media/', null=True, blank=True)

class Buyer(models.Model):
    user = models.OneToOneField(NormalUser, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=20, null=True)
    company_profile = models.FileField(upload_to='media/', null=True, blank=True)