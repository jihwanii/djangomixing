from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug']
    prepopulated_fields = {'slug':['name']} # 값을 입력시 저절로 값이 입력되는 기능

admin.site.register(Category, CategoryAdmin)