from decimal import Decimal
from django.conf import settings

from shop.models import Product
from coupon.models import Coupon

class Cart(object):
    def __init__(self, request): # 초기화 작업
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self): # iter를 사용할 때 list, dic는 몇개나 있냐 등을 알려주는 역활
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self): # for 문등 문법을 사용할 때에 어떠한 방식으로 사용할 것인 지 알려주는 역활
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids) # id__in= 이 안에 있는 아이디만 주세요~

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item # yield 공부 필요

    # 정보 추가 함수
    def add(self, product, quantity=1, is_update=False): # 장바구니는 업데이트는 필요하지 않고 상품을 추가만 하는 것이라서 is_update=False.
        product_id = str(product.id)
        if product_id not in self.cart: # 제품 정보가 없을 때
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)}

        if is_update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    # 정보 저장 함수
    def save(self):
        self.session[settings.CART_ID] = self.cart # session에 정보 update
        self.session.modified = True # 이 코드를 작성하지 않으면 업데이트는 이루어지지않음.

    # 정보를 삭제해주는 함수
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del(self.cart[product_id])
            self.save()

    # 정보를 비워주는 함수
    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session['coupon_id'] = None
        self.session.modified = True

    # 모든 상품 정보를 가져오는 함수
    def get_product_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # 쿠폰 내용을 가져오는 함수
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    # 얼마나 할인 되는 지 알려주고 할인 금액을 알려주는 함수
    def get_discount_total(self):
        if self.coupon: #property 때문에 coupon 정보를 받아 올 수 있음.
            if self.get_product_total() >= self.coupon.amount:
                return self.coupon.amount
        return Decimal(0)

    # get_product_total 함수와 get_discount_total 함수를 가져와 실제 결제할 금액을 알려주는 함수
    def get_total_price(self):
        return self.get_product_total() - self.get_discount_total()