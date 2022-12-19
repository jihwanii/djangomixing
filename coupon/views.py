from django.shortcuts import render

from django.shortcuts import redirect
from django.utils import timezone # 이것을 사용해야 사용자가 접속한 국가의 시간에 맞게 정보를 가져올 수 있음.
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import AddCouponForm
# Create your views here.

@require_POST
def add_coupon(request):
    now = timezone.now()
    form = AddCouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']

        try: # code__iexact 쿠폰의 대소문자 일치 확인 , use_from__lte 모델의 use_to 보다 날짜가 늦는 지 확인, use_to__gte 모델의 use_to 보다 날짜가 앞섰는 지 확인
            coupon = Coupon.objects.get(code__iexact=code, use_from__lte=now, use_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart:detail')