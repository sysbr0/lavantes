# customers/models.py

from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
from django.db.models import Sum



class Costomers(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_customers')
    image = models.URLField(blank=True, null=True)
    tex = models.BigIntegerField(blank=True, null=True) 
    email = models.EmailField(blank=True, null=True)
    number = models.CharField(max_length=255 ,  null=True)
    is_company = models.BooleanField(default=0)
    company = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    profile_image = models.ImageField(upload_to='costomers/', blank=True, null=True)  # Image field for profile image
    balanceTr = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    balanceUsd = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        ordering = ['-updated_at']  # Default ordering by primary key
  


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        """Override the save method to update the updated_at field."""
        self.updated_at = timezone.now()  # Update the updated_at field
        super().save(*args, **kwargs)  # Call the original save method


    def get_total_price_usd(self):
        """Returns the total sum of price for all UdsBills related to this customer."""
        # Import UdsBills from the bill app
        from biles.models import UdsBills 

        total_price = UdsBills.objects.filter(customer=self).aggregate(total=Sum('price'))['total']
        
        return total_price if total_price else 0
    


    def get_total_payments_usd(self):
        """Calculate the total amount of USD payments made by the customer."""
        from money.models import CustomerPaymentUsd  # Assuming a similar model for USD payments
        total_payments_usd = CustomerPaymentUsd.objects.filter(customer=self).aggregate(Sum('amount'))['amount__sum'] or 0
        return total_payments_usd
    
    
    def get_total_price_tr(self):
        """Returns the total sum of price for all UdsBills related to this customer."""
        # Import UdsBills from the bill app
        from biles.models import TrBills 

        total_price = TrBills.objects.filter(customer=self).aggregate(total=Sum('price'))['total']
        return total_price if total_price else 0



    def get_total_payments_tl(self):
        """Calculate the total amount of TL payments made by the customer."""
        from money.models import CustomerPaymentTl  # Import to avoid circular import
        total_payments_tl = CustomerPaymentTl.objects.filter(customer=self).aggregate(Sum('amount'))['amount__sum'] or 0
        return total_payments_tl
    

    def calculate_balance_tl(self):
        """Calculate the balance in TL (Bills - Payments)."""
        self.balanceTr = self.get_total_price_tr() - self.get_total_payments_tl()
        self.save()
        return  self.balanceTr
    

    def calculate_balance_usd(self):
        """Calculate the balance in TL (Bills - Payments)."""
        self.balanceUsd = self.get_total_price_usd() - self.get_total_payments_usd()
        self.save()
        return  self.balanceUsd
    


        



