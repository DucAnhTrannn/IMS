from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone

from .models import Customer, Product, Order, Invoice
from .forms import CustomerForm, ProductForm, OrderForm, InvoiceForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'authentication/login.html', {'error_message': 'Invalid login credentials'})
    return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


###### ------------------------------------ CUSTOMER ------------------------------------ ######
@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer/customer_list.html', {'customers': customers})

@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer/add_customer.html', {'form': form})

@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer/edit_customer.html', {'form': form, 'customer': customer})

@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customer/delete_customer.html', {'customer': customer})



###### ------------------------------------ PRODUCT ------------------------------------ ######
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product/delete_product.html', {'product': product})



###### ------------------------------------ ORDER ------------------------------------ ######
@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order/order_list.html', {'orders': orders})

@login_required
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'order/add_order.html', {'form': form})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'order/edit_order.html', {'form': form, 'order': order})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'order/delete_order.html', {'order': order})



###### ------------------------------------ INVOICE ------------------------------------ ######
@login_required
def invoice_list(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    invoices = Invoice.objects.all()
    # print(invoices.query)

    if query:
        invoices = invoices.filter(
            Q(customer__name__icontains=query) |
            Q(customer__phone__icontains=query)
        ).distinct()

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            invoices = invoices.filter(date_payment__gte=start_date)
        except ValueError:
            pass  # Handle invalid date format or value
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            invoices = invoices.filter(date_payment__lte=end_date)
        except ValueError:
            pass  # Handle invalid date format or value

    return render(request, 'invoice/invoice_list.html', {'invoices': invoices, 'query': query, 'start_date': start_date, 'end_date': end_date})

@login_required
def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'invoice/add_invoice.html', {'form': form})

@login_required
def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'invoice/edit_invoice.html', {'form': form, 'invoice': invoice})

@login_required
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'invoice/delete_invoice.html', {'invoice': invoice})

@login_required
def export_invoices_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="invoices.csv"'

    invoices = Invoice.objects.all()

    writer = csv.writer(response)
    writer.writerow(['Invoice ID', 'Date Payment', 'Due Date', 'Total Payment', 'Order ID'])  # Add headers

    for invoice in invoices:
        writer.writerow([invoice.invoice_id, invoice.date_payment, invoice.total_payment, invoice.order.order_id])

    return response

@login_required
def export_invoices_pdf(request):
    template_path = 'invoice/invoices_pdf_template.html'
    context = {'invoices': Invoice.objects.all()}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoices.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response



###### ------------------------------------ STATISTICS ------------------------------------ ######
@login_required
def statistics(request):
    # Calculate payment status
    paid_invoices_count = Invoice.objects.filter(paid=True).count()
    total_invoices_count = Invoice.objects.count()
    unpaid_invoices_count = total_invoices_count - paid_invoices_count
    if total_invoices_count != 0:
        paid_percentage = (paid_invoices_count / total_invoices_count) * 100
    else:
        paid_percentage = 0

    unpaid_percentage = 100 - paid_percentage

    # Calculate total sales volume
    total_sales = Invoice.objects.aggregate(Sum('total_payment'))['total_payment__sum'] or 0

    # Calculate on-time percentage
    on_time_invoices_count = Invoice.objects.filter(date_payment__lte=timezone.now()).count()
    on_time_percentage = (on_time_invoices_count / total_invoices_count) * 100 if total_invoices_count > 0 else 0

    context = {
        'paid_percentage': paid_percentage,
        'unpaid_percentage': unpaid_percentage,
        'total_sales': total_sales,
        'on_time_percentage': on_time_percentage,
    }

    return render(request, 'statistic/statistics.html', context)

@login_required
def payment_status(request):
    paid_invoices = Invoice.objects.filter(paid=True)
    unpaid_invoices = Invoice.objects.filter(paid=False)

    context = {
        'paid_invoices': paid_invoices,
        'unpaid_invoices': unpaid_invoices,
    }

    return render(request, 'statistic/payment_status.html', context)