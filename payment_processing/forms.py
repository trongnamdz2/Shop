from django import forms


METHOD_CHOICES = [
    ('face-to-face', 'Thanh toán khi nhận hàng')
]

class AddressForm(forms.Form):
    full_name = forms.CharField(required=True, label='Tên người nhận')
    address = forms.CharField(widget=forms.Textarea(), max_length=100, required=True, label='Địa chỉ')
    sdt = forms.IntegerField(label='Số điện thoại')
    method = forms.ChoiceField(choices=METHOD_CHOICES, label='Cổng thanh toán', required=True)

    def clean(self):
        super(AddressForm, self).clean()
        
        phone_numb = self.cleaned_data['sdt']

        if len(str(phone_numb)) > 13:
            self._errors['sdt'] = self.error_class(['Số điện thoại không được quá 13 kí tự'])

        return self.cleaned_data