from django.db import models
from biles.models import ProductHam
from django.utils import timezone

# Create your models here.


class Message(models.Model):
    sender_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_name} - {self.subject}"
    



 
class Product_imges(models.Model):
    product_ham = models.ForeignKey(ProductHam, related_name="select_ham_foruplode", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Product_imges/', blank=True, null=True)  # Image field for profile image
    active = models.BooleanField(default=True)  # True for active, False for inactive
    date = models.DateField(default=timezone.now)
    name = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.id} - {self.product_ham.product_name} "
    

    def save(self, *args, **kwargs):
        # Set the 'name' field before saving
        self.name = f"{self.product_ham.product_name}  "
        super(Product_imges, self).save(*args, **kwargs)
    
    



 
class Swapper_Imges(models.Model):
    image = models.ImageField(upload_to='swapper_imges/', blank=True, null=True)  
    active = models.BooleanField(default=True)  # True for active, False for inactive
    date = models.DateField(default=timezone.now)
    name = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.name} "

    




class Address(models.Model):
    uid = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.uid
    







from django.db import models
from django.conf import settings

class MessageLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_messge')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.message[:50]}"