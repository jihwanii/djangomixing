from django import forms

# 클라이언트 화면에 입력폼을 만들어주기 위해
# 클라이언트가 입력한 데이터에 댄한 천처리

class AddProductForm(forms.Form):
    quantity = forms.IntegerField()

    # BooleanField는 required=False로 지정해 주지 않으면 True, False 값을 받아오늘 필드임에도 불구하고 값을 받지않고 넘어감. 그래서 꼭!!! required=False 작성하기!!
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)