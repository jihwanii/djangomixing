from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

from shop.models import Product
from coupon.models import Coupon


# Create your models here.
# 추후에 orderstatus 필드 또는 모델을 만들어 고객들에게 주문상태를알려주는 기능을 추가하여야함.

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, blank=True)
    #success = models.BooleanField(default=False) # view에서 success 줄 실행 시 필요
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name='order_coupon', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])

    class Meta:
        ordering = ['-created'] # 최신 데이터가 위에 올라오도록 '-'를 붙여줌.

    # 외부에서 엑세스 할 필요가 있을 때 사용함.
    # 관리자 페이지 또는 다른 곳에서 출력시 어떤 내용을 보여 줄 것인 가를 정함.
    # 특정 필드를 찍어서 불러오는 것이 아니라 객체 자체를 출력했을 때 나오는 코드 / 장고 코드 아님! 파이썬 코드임.
    def __str__(self):
        return f'Order {self.id}'

    # 주문 번호와 부문 금액을 비교 하는 것
    # 해커 또는 오류를 확인하고 방지하는 목적

    def get_total_product(self):
        return sum(item.get_item_price() for item in self.items.all())

    def get_total_price(self):
        total_product = self.get_total_product()
        return total_product - self.discount

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') # 오타 수정 해라
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_item_price(self):
        return self.price * self.quantity

# 새로 transaction을 만들었을 때 Order 정보를 하나 갖게해주는 역활 / Manager
import hashlib
from .iamport import payments_prepare, find_transaction
class OrderTransactionManager(models.Manager):
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문 정보 오류")
        # 유니크한 주문 구문 번호를 만들기 위한 과정 iamport에 보내기 위한
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest() # sha1()안에 있는 데이터를 sha1으로 암호화 하고 hexdigest로 바꾼다는 코드
        email_hash = str(order.email).split("@")[0]
        final_hash = hashlib.sha1((order_hash+email_hash).encode('utf-8')).hexdigest()[:10] # order_hash + email_hash의 암호를 다시 sha1으로 암호화 하여 hexdigest로 바꾸고 앞의 10글자를 따겠다는 코드
        merchant_order_id = str(final_hash) # 동영상 강의에서 변경
        payments_prepare(merchant_order_id, amount)

        transaction = self.model(
            order=order,
            merchant_order_id=merchant_order_id,
            amount=amount
        )

        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status

        try:
            transaction.save()
        except Exception as e:
            print("save error", e)

        return transaction.merchant_order_id

    def get_transaction(self, merchant_order_id):
        result = find_transaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None

# 결재에 대한 정보를 품고 있음.
class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) # 오타 수정 해라
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True) # 10글자로 줄여도 됨, 이유는 위에서 10글자만 따오기 때문에
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)
    type = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    #success = models.BooleanField(default=False)
    objects = OrderTransactionManager()

    def __str__(self):
        return str(self.order.id)

    class Meta:
        ordering = ['-created']


def order_payment_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        import_transaction = OrderTransaction.objects.get_transaction(merchant_order_id=instance.merchant_order_id)
        merchant_order_id = import_transaction['merchant_order_id']
        imp_id = import_transaction['imp_id']
        amount = import_transaction['amount']

        local_transaction = OrderTransaction.objects.filter(merchant_order_id=merchant_order_id, transaction_id=imp_id, amount=amount).exists()

        if not import_transaction or not local_transaction:
            raise ValueError("비정상 거래입니다.")

# 컴퓨터야 니가 어떠한 할 일을 다하면 나한테 알려줘~! => signals 임.
from django.db.models.signals import post_save
post_save.connect(order_payment_validation, sender=OrderTransaction) # sender를 작성해주면 sender에서 save가 일어날때만 시그널을 보냄.