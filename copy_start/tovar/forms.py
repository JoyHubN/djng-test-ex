from django import forms

class TovarAdd(forms.Form):
    quantity = forms.IntegerField(
        label="Количество",
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={'id': 'quantity', 'class': 'form-control'})
    )

class OrderCheckoutForm(forms.Form):
    password = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Введите ваш текущий пароль для подтверждения заказа."
    )
