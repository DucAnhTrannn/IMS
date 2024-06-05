from django import forms
from .models import Customer, Product, Order, Invoice

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer email address'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'unit_price', 'stock_quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product unit price'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product stock quantity'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['date', 'order_value', 'customer', 'product']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Select the order date'}),
            'order_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the order value'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'order_value': 'Enter the order value in dollars.',
        }

    def clean_order_value(self):
        order_value = self.cleaned_data['order_value']
        if order_value < 0:
            raise forms.ValidationError("Order value cannot be negative.")
        return order_value

    
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date_payment', 'due_date', 'total_payment', 'order', 'customer', 'paid']
        widgets = {
            'date_payment': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Select the date when payment was made'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Select the due date for payment'}),
            'total_payment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the total payment amount'}),
            'order': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'date_payment': 'Date of Payment',
            'due_date': 'Due Date',
            'total_payment': 'Total Payment',
            'order': 'Order',
            'customer': 'Customer',
            'paid': 'Paid',
        }

