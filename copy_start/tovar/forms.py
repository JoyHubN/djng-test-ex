from django import forms

class TovarAdd(forms.Form):
    quantity = forms.IntegerField(
        label="Количество",
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={'id': 'quantity'})
    )
