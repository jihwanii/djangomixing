import requests
from django.conf import settings


# api와 secret key를 가지고 로그인 처리를 하는 함수, 이를 실행하려면 토큰이 매번 새로 필요한데, 토큰을 매번 새로 받아서 로그인을 실행하는 함수
def get_token():
    access_data = {
        'imp_key':settings.IAMPORT_KEY,
        'imp_secret':settings.IAMPORT_SECRET
    } # 아래 url에서 token을 가져오기 위하여 imp_key, imp_secret정보를 저장하여 가져올 수 있도록 하는 코드 / imp_key, imp_secret는 iamport에서 입력해달라고 한 양식 
    url = "https://api.iamport.kr/users/getToken" # 정보를 받아오고자하는 url / 이 url은 기본적으로 iamport에서 token을 받아올 수 있도록 주어진 url
    req = requests.post(url, data=access_data) # requests.post로 url을 통해 받아온 정보를 req의 변수에 저장 / data=access_data는 imp_key, imp_secret의 정보를 받아올 수 있도록 하는 코드
    access_res = req.json() #req를 json형식으로 변환 및 해석

    if access_res['code'] is 0: # access_res에서 제대로 응답이 왔을 시 참의 결과값을 반환 / * http'code'가 아니라 iamport에서 약속한 코드.
        return access_res['response']['access_token'] # 로그인에 필요한 토큰값!을 받아오는 코드
    else:
        return None

# 어떤 오더 아이디로 얼마만큼의 금액으로 결제를 요청할꺼에요라고 미르 등록을 하는 함수
def payments_prepare(order_id, amount, *args, **kwargs):
    access_token = get_token() # 토큰을 가져옴
    if access_token:
        access_data = {
            'merchant_uid':order_id, # 우리가 정한 order_id
            'amount':amount # 우리가 정한 amount
        }
        url = "https://api.iamport.kr/payments/prepare" # 이것 또한 iamport에서 지정해준 url
        headers = {
            'Authorization':access_token # 이렇게 hearder를 안 불러오면 오류가 뜸 
        }
        req = requests.post(url, data=access_data, headers=headers) # post 시 data와 hearders를 확인하고 받아 와야함
        res = req.json()
        if res['code'] != 0: # is not 보다는 !=으로 조건을 거는 것이 더 정확함 / 데이터가 없는 지 확인 하는 함수.
            raise ValueError("API 통신 오류")
    else:
        raise ValueError("토큰 오류")

# 주문자가 주문한 금액만큼 결제가되었는지 확인하고 결제완료로 변경해주는 함수. 이 기능이 없어도 결제는 진행이 되지만, 확인을 안하니 사기를 당할 수 있음. 사기를 방지하고자 필요로 하는 함수.
def find_transaction(order_id, *args, **kwargs):
    access_token = get_token()
    if access_token:
        url = "https://api.iamport.kr/payments/find/"+order_id
        headers = {
            'Authorization':access_token
        }
        req = requests.post(url, headers=headers)
        res = req.json()
        if res['code'] == 0: # 
            context = {
                'imp_id':res['response']['imp_uid'],
                'merchant_order_id':res['response']['merchant_uid'],
                'amount':res['response']['amount'],
                'status':res['response']['status'],
                'type':res['response']['pay_method'],
                'receipt_url':res['response']['receipt_url']
            }
            return context # 데이터를 가져올때는 최대한 변환되지 않은 서버의 데이터를 가져오는 것이 좋음 
        else:
            return None
    else:
        raise ValueError("토큰 오류")