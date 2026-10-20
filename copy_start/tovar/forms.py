from django import forms
from .models import Document
from .validate import validate_file_size

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

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']

UploadFile = DocumentForm


