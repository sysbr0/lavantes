import uuid
# Create your models here.
from django.db import models
from django.utils import timezone
from customers.models import Costomers
from django.db.models import Sum



    



from django.utils.timezone import now


class MoneySource(models.Model):
    SOURCE_CHOICES = [
        ('cash', 'Cash Account'),
        ('bank', 'Bank Account'),
        ('company_bank', 'Company Bank Account'),
    ]

    name = models.CharField(max_length=100)  # e.g., "Cash Account", "Bank Account"
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    source_type = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='cash')

    def __str__(self):
        return f"{self.name} ({self.source_type}) - Balance: {self.balance}"
    





class GeneralPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)
    note = models.TextField()  # To store notes about the payment
    source = models.ForeignKey(MoneySource, on_delete=models.CASCADE , default=None)
    payment_token = models.UUIDField(default=uuid.uuid4, unique=True)  # Unique payment token

    def __str__(self):
        return f" General Payment from {self.source.name} of {self.amount} on {self.date} - {self.note}"
    

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.source is None:
                # Set default source as cash if not provided
                self.source = MoneySource.objects.filter(source_type='cash').first()
                if self.source is None:
                    raise ValueError('No default cash source available')

            #if self.source.balance < self.amount:
              #  raise ValueError('Insufficient funds in source')
                
            # Update the balance
            self.source.balance -= self.amount
            self.source.save()

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Restore the balance before deleting
        self.source.balance += self.amount
        self.source.save()
        super().delete(*args, **kwargs)






class CustomerPaymentTl(models.Model):

    customer = models.ForeignKey(Costomers, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)
    note = models.TextField(null=True, blank=True)  # Optional note for the payment
    source = models.ForeignKey(MoneySource, on_delete=models.CASCADE, default=None)
    payment_token = models.UUIDField(default=uuid.uuid4, unique=True)  # Unique payment token
    image = models.ImageField(upload_to='Customer/pymnets/tl/', blank=True, null=True)

    def __str__(self):
        return f"Customer Payment of {self.amount} by {self.customer.name} on {self.date}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only update balance when creating a new payment
            if self.source is None:
                self.source = MoneySource.objects.filter(source_type='cash').first()
                if self.source is None:
                    raise ValueError('No default cash source available')
                

            self.source.balance += self.amount
            self.source.save()
            
        self.customer.calculate_balance_tl()
        self.customer.save()
         

            # Update the balance of the source
           

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restore the balance before deleting
        self.customer.calculate_balance_tl()
        self.customer.save()
        
        self.source.balance -= self.amount
   
    
        self.source.save()
        super().delete(*args, **kwargs)



    




class CustomerPaymentUsd(models.Model):
    customer = models.ForeignKey(Costomers, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)
    note = models.TextField(null=True, blank=True)  # Optional note for the payment
    source = models.ForeignKey(MoneySource, on_delete=models.CASCADE, default=None)
    payment_token = models.UUIDField(default=uuid.uuid4, unique=True)  # Unique payment token
    image = models.ImageField(upload_to='Customer/pymnets/usd/', blank=True, null=True)

    def __str__(self):
        return f"Customer Payment of {self.amount}  by {self.customer.name} on {self.date}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only update balance when creating a new payment
            if self.source is None:
                self.source = MoneySource.objects.filter(source_type='cash').first()
                if self.source is None:
                    raise ValueError('No default cash source available')
        

            # Update the balance of the source
            
     
            self.source.balance += self.amount
            self.source.save()

        self.customer.calculate_balance_usd()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Restore the balance before deleting
        self.customer.calculate_balance_usd()
        self.source.balance -= self.amount
        self.source.save()
        super().delete(*args, **kwargs)



    def get_customer_total(self):
        total = CustomerPaymentUsd.objects.filter(customer=self.customer).aggregate(Sum('amount'))
        return total['amount__sum'] if total['amount__sum'] is not None else 0








from employe.models import Employee

class BasePayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    note = models.TextField()
    payment_token = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True


    







class sorcePyment(BasePayment):
    source = models.ForeignKey(MoneySource, on_delete=models.CASCADE)







class EmployePayment(sorcePyment):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=None)


