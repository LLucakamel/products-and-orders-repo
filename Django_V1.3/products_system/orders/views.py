from django.shortcuts import render, redirect
from .models import Order
from products.models import Product
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
import datetime

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'mm/dd/yyyy'}),
        }
        
    def clean_quantity(self):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')
        if product and quantity > product.stock:
            raise ValidationError(f"Only {product.stock} available. Cannot order more than that.")
        return quantity

def order_list(request):
    orders = Order.objects.all()
    employee_name = request.GET.get('employee_name')
    order_code = request.GET.get('order_code')
    product_name = request.GET.get('product_name')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    query = Q()
    if employee_name:
        query |= Q(employee__name__icontains=employee_name)
    if order_code:
        query |= Q(product__code__icontains=order_code)  # Changed here to refer to code field in Product model
    if product_name:
        query |= Q(product__name__icontains=product_name)
    if date_from:
        query &= Q(order_date__gte=datetime.datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query &= Q(order_date__lte=datetime.datetime.strptime(date_to, '%Y-%m-%d'))

    orders = orders.filter(query)

    return render(request, 'orders/orders_list.html', {'orders': orders})

def order_create(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        product = order.product
        product.refresh_from_db()  # Refresh product data from the database
        print(f"Stock before deduction: {product.stock}")  # Log stock value before deduction
        product.stock -= order.quantity
        product.save()
        print(f"Stock after deduction: {product.stock}")  # Log stock value after deduction
        order.save()
        return redirect('order_list')
    return render(request, 'orders/orders_form.html', {'form': form})

def order_update(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        return redirect('order_list')
    return render(request, 'orders/orders_form.html', {'form': form})

def order_delete(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/orders_confirm_delete.html', {'object': order})

# New views for reviewing and updating order status
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import OrderReviewForm

def review_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderReviewForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders_review_list')
    else:
        form = OrderReviewForm(instance=order)
    return render(request, 'orders/review_order.html', {'form': form, 'order': order})

def review_order_list(request):
    orders = Order.objects.filter(status='pending')
    return render(request, 'orders/review_order_list.html', {'orders': orders})