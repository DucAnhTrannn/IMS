from django.conf import settings 

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import send_mail
from ims_app.models import Invoice

class Command(BaseCommand):
    help = 'Sends reminder emails for invoices'

    def handle(self, *args, **options):
        # Logic to identify invoices approaching payment deadline or status changes
        invoices_due = Invoice.objects.filter(due_date__lte=timezone.now(), paid=False)
        invoices_status_change = Invoice.objects.exclude(paid=False)

        # Send reminder emails for invoices approaching payment deadline
        for invoice in invoices_due:
            self.send_payment_due_email(invoice)

        # Send reminder emails for invoices undergoing status changes
        for invoice in invoices_status_change:
            self.send_status_change_email(invoice)

    def send_payment_due_email(self, invoice):
        subject = 'Payment Due Reminder'
        message = render_to_string('email_templates/payment_due.html', {'invoice': invoice})
        send_mail(subject, message, settings.EMAIL_HOST_USER, [invoice.customer.email])

    def send_status_change_email(self, invoice):
        subject = 'Invoice Status Change'
        message = render_to_string('email_templates/status_change.html', {'invoice': invoice})
        send_mail(subject, message, settings.EMAIL_HOST_USER, [invoice.customer.email])

