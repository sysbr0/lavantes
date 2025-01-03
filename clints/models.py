from django.db import models


from django.conf import settings
import uuid

from django.db.models import Sum
from money.models import GeneralPayment , MoneySource

from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator

class clints(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_clint')
    tex = models.BigIntegerField(blank=True, null=True) 
    email = models.EmailField(blank=True, null=True)
    number = models.CharField(max_length=255 ,  null=True)
    is_company = models.BooleanField(default=0)
    company = models.TextField(blank=True, null=True)
    total_paied = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    total_buy = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999)], default=0)
    balance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999)], default=0)
    address = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=36, unique=True, default=uuid.uuid4)
    profile_image = models.ImageField(upload_to='clints/', blank=True, null=True)  # Image field for profile image


    def __str__(self):
        return self.name
    



    def get_total(self):
        # Import UdsBills from the bill app
        from main.models import GeneralBuying

        total_price = GeneralBuying.objects.filter(client=self).aggregate(total=Sum('price'))['total']
        self.total_buy= total_price
        self.save()
      
       
        
        return total_price if total_price else 0
    
    

    def get_total_payment(self):
        # Import UdsBills from the bill app
        from main.models import GeneralBuying

        total_price = ClintPayment.objects.filter(clint=self).aggregate(total=Sum('amount'))['total']
        self.total_paied= total_price
        self.save()
       
        
        return total_price if total_price else 0
    


    def save(self, *args, **kwargs): 
        # Save the instance first to ensure it's in the database
        is_new = self.pk is None  # Check if this is a new instance
        super().save(*args, **kwargs)

        if is_new:
            # Update calculated fields after the instance is saved
            self.total_buy = self.get_total()
            self.total_paied = self.get_total_payment()
            self.balance = self.total_buy - self.total_paied
            super().save(update_fields=['total_buy', 'total_paied', 'balance'])



    def calculate(self):
        self.balance = self.get_total() - self.get_total_payment()
        self.save()
        return self.balance


    
    def MakePyment(self , amount):
        pass



    def RemovePyment(self , amount):
        pass
       
    

    






    



from django.utils.timezone import now


class ClintPayment(models.Model):
    source = models.ForeignKey(MoneySource, on_delete=models.CASCADE , default=None)
    clint = models.ForeignKey(clints, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)
    note = models.TextField(default="None")
    payment_token = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)  # Use default for automatic generation
    image = models.ImageField(upload_to='clints/pymnets/', blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} to {self.clint.name} on {self.date}"
    

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new record
            super().save(*args, **kwargs)  # Save the EmployeePayment first

            # Create a general payment record
            note = f"Payment to clint  {self.clint.name}, amount: {self.amount}, note: {self.note}"
            
   
            general_payment = GeneralPayment.objects.create(
                amount=self.amount,
                date=self.date,
                note=note,
                source=self.source
            )
            
            self.payment_token = general_payment.payment_token  # Set the payment token
            self.clint.get_total_payment()
        



            

        super().save(*args, **kwargs)  # Save the EmployeePayment with the toke



    def delete(self, *args, **kwargs):
        try:
            general_payment = GeneralPayment.objects.get(payment_token=self.payment_token)
            general_payment.delete()  # Delete the corresponding GeneralPayment
            self.clint.get_total_payment()
        except GeneralPayment.DoesNotExist:
            pass  # No corresponding GeneralPayment found

        super().delete(*args, **kwargs)

    def remove(self):
        self.delete()