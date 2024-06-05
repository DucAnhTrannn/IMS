from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    order_value = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order: {self.order_id}, Product: {self.product}, Customer: {self.customer}"

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    date_payment = models.DateTimeField()
    due_date = models.DateField()
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Invoice {self.invoice_id}'

class Debt(models.Model):
    debt_id = models.AutoField(primary_key=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'Debt {self.debt_id}'

class DebtPayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)

    def __str__(self):
        return f'Payment {self.payment_id}'
