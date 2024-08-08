from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Order
from products.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'due_date',]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_quantity(self):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')
        if product and quantity > product.stock:  # Ensure the stock field exists in the Product model
            raise ValidationError(f"Only {product.stock} available. Cannot order more than that.")
        return quantity

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']