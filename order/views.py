from django.shortcuts import render, get_object_or_404
from .models import *
from cart.cart import Cart
from .forms import *

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        # 입력받은 정보를 후처리
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) # commit=False 쿼리가 두번 날아가지 않게 효율적으로 해줌
            if cart.coupon:
                order.coupon = cart.coupon
                #order.discount = cart.coupon.amount # 로직 1
                order.discount = cart.get_discount_total() # 로직 2 이 로직이 더 정확하고 안전함.
                order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'order/created.html', {'order':order})
    else: # 주문자 정보를 입력받는 페이지
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart':cart, 'form':form}) # return 이 else와 같이 있는 이유는 최상단 if문에서 오류가 발생하였을 시 정보를 잘못 입력하였다는 안내와 다시 새폼으로 안내하기 위하여 같이 있음.

# JS 동작하지 않는 환경에서도 주문은 가능해야한다.
def order_complete(request):
    order_id = request.GET.get('order_id')
    #order = Order.objects.get(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/created.html', {'order':order})

from django.views.generic.base import View
from django.http import JsonResponse

class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인이 여부 판단
            return JsonResponse({"authenticated":False}, status=403)

        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.get_discount_total()
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            data = {
                "order_id":order.id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated: # 로그인이 여부 판단
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount
            )
        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works":True,
                "merchant_id":merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated": False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)

        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            #trans.success = True # 모델 success 주석 풀고 실행
            trans.save()
            order.paid = True
            order.save()

            data = {
                "works":True
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/admin/detail.html', {'order':order})

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint # pdf 파일을 만들때 필요한 라이브러리

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order/admin/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf') # 브라우저야 pdf 내용이 시작될꺼야~
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf' # 파일 이름 설정
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0]+'/css/pdf.css')]) # local /css/pdf.css에서 불러오는 것임.
    return response