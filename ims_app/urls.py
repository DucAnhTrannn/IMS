from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('customer_list/', views.customer_list, name='customer_list'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),

    path('product_list/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('order_list/', views.order_list, name='order_list'),
    path('add_order/', views.add_order, name='add_order'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),

    path('invoice_list/', views.invoice_list, name='invoice_list'),
    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('edit_invoice/<int:invoice_id>/', views.edit_invoice, name='edit_invoice'),
    path('delete_invoice/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('export_invoices_csv/', views.export_invoices_csv, name='export_invoices_csv'),
    path('export_invoices_pdf/', views.export_invoices_pdf, name='export_invoices_pdf'),

    path('statistics/', views.statistics, name='statistics'),
    path('statistics/payment-status/', views.payment_status, name='payment_status'),
]
