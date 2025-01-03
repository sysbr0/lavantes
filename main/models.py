from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from clints.models import clints
from django.utils import timezone
from biles.models import Jar , Package ,Jar_off , ProductHam
import uuid
from django.conf import settings
from django.core.exceptions import ValidationError

from django.utils.timezone import now

class BuyingType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    Name_En = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class GeneralBuying(models.Model):
    client = models.ForeignKey(clints, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_general_buying')
    buying_type = models.ForeignKey(BuyingType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    updated_at = models.DateTimeField(auto_now=True)  # Set default to January 1, 2024
    notee = models.CharField(max_length=255, blank=True, null=True )
    is_pyed = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-pk']  # Default ordering by primary key

    def __str__(self):
        return f"{self.client.name} - {self.buying_type.name}"
    
    def calculate_total(self):
        # Calculate total price from all inner transactions
        total = sum(inner.total for inner in self.inner_transactions.all())
        self.price = total
        
        self.save()
        self.client.get_total()
        


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now().date()


        self.client.save()

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
            # Find the corresponding GeneralPayment using the payment_token
        self.client.save()
        super().delete(*args, **kwargs)

    def note(self):
         return f"General Buying {self.pk} - {self.buying_type.name}  - {self.client} "
        

        






class GeneralInner(models.Model):
    general_buying = models.ForeignKey(GeneralBuying, on_delete=models.CASCADE, related_name='inner_transactions')
    description = models.CharField(max_length=255 ,default="none")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=0)
    created_at = models.DateField(default=timezone.now)
    note = models.CharField(max_length=255, blank=True, null=True )
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    token = models.UUIDField(default=uuid.uuid4, unique=True)  # Unique payment token


    def __str__(self):
        return f"{self.description} - {self.price}"

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now().date()

        # Update total based on price and amount
        self.total = self.amount * self.price
        super().save(*args, **kwargs)
        # Update the total in the related GeneralBuying instance
        self.general_buying.calculate_total()



            
    def delete(self, *args, **kwargs):
        print(self.note)
        super().delete(*args, **kwargs)
        # Update the total in the related GeneralBuying instance
        self.general_buying.calculate_total()

    





class JarInner(models.Model):
        general_buying = models.ForeignKey(GeneralBuying, on_delete=models.CASCADE, related_name='inner_jar')
        jar = models.ForeignKey(Jar, related_name="select_jar_to_buy", on_delete=models.CASCADE)
        amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=0)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        note = models.CharField(max_length=255, blank=True, null=True )
        token = models.UUIDField(editable=False, unique=True , null=True)  # Unique payment token
        created_at = models.DateField(default=timezone.now)
        total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        def __str__(self):
          return f"{self.jar} - {self.price}"


        def save(self, *args, **kwargs):
          if not self.created_at:
                 self.created_at = timezone.now().date()
          self.total = self.amount * self.price
          note = f"{self.jar.jar_name}  "
    
          if not self.pk:  # Check if this is a new record
                super().save(*args, **kwargs) 
                 # Save the EmployeePayment first
                

                generalInner = GeneralInner.objects.create(
                    general_buying= self.general_buying, 
                    amount=self.amount,
                    price=self.price,
                    description=note,
                    note= "pisies",
           
                    created_at=self.created_at,


   
                )



                
                
                self.token = generalInner.token  # Set the payment token
                self.jar.add_to_stock(self.amount)

          super().save(*args, **kwargs)


         
        def delete(self, *args, **kwargs):
        # Delete the corresponding GeneralInner instance
            try:
                
                general_inner = GeneralInner.objects.get(token=self.token)
                print("exist")
                general_inner.delete()
            except GeneralInner.DoesNotExist:
                print("dosnt exist")
               

            # Update stock if necessary
            self.jar.remove_from_stock(self.amount)
            print("sucsflly")

            super().delete(*args, **kwargs)

            








class Jar_off_Inner(models.Model):
        general_buying = models.ForeignKey(GeneralBuying, on_delete=models.CASCADE, related_name='inner_jar_of')
        jar_of = models.ForeignKey(Jar_off, related_name="select_jar_of_to_buy", on_delete=models.CASCADE)
        amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=0)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        note = models.CharField(max_length=255, blank=True, null=True )
        token = models.UUIDField(editable=False, unique=True , null=True)  # Unique payment token
        created_at = models.DateField(default=timezone.now)
        total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        def __str__(self):
          return f"{self.jar_of.jar_name} - {self.amount} - {self.price}"


        def save(self, *args, **kwargs):
          if not self.created_at:
                 self.created_at = timezone.now().date()
          self.total = self.amount * self.price
          note = f"{self.jar_of.jar_name}"
          
          if not self.pk:  # Check if this is a new record
                super().save(*args, **kwargs) 
                 # Save the EmployeePayment first
                

                generalInner = GeneralInner.objects.create(
                    general_buying= self.general_buying, 
                    amount=self.amount,
                    price=self.price,
                    description=note,
                    note="picess",

           
                    created_at=self.created_at,

                  
                )
                
                self.token = generalInner.token  # Set the payment token
                self.jar_of.add_to_stock(self.amount)

          super().save(*args, **kwargs)

        



        def delete(self, *args, **kwargs):
            # Find the corresponding GeneralPayment using the payment_token
            try:
                general_payment = GeneralInner.objects.get(token=self.token)
                general_payment.delete()  # Delete the GeneralPayment record

                self.jar_of.remove_from_stock(self.amount)
      
            except GeneralInner.DoesNotExist:
                pass  # If no corresponding GeneralPayment is found, continue with the deletion

            super().delete(*args, **kwargs)
        





class PakageInner(models.Model):
        general_buying = models.ForeignKey(GeneralBuying, on_delete=models.CASCADE, related_name='inner_pakage')
        pakage = models.ForeignKey(Package, related_name="select_Pakage_to_buy", on_delete=models.CASCADE)
        amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=0)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        note = models.CharField(max_length=255, blank=True, null=True )
        token = models.UUIDField(editable=False, unique=True , null=True)  # Unique payment token
        created_at = models.DateField(default=timezone.now)
        total = models.DecimalField(default=0, max_digits=10, decimal_places=2)


        def save(self, *args, **kwargs):
          if not self.created_at:
                 self.created_at = timezone.now().date()
          self.total = self.amount * self.price

        
          note = f"{self.pakage.package_name}  : {self.note}"
 


          if not self.pk:  # Check if this is a new record
                super().save(*args, **kwargs) 
                 # Save the EmployeePayment first
                

                generalInner = GeneralInner.objects.create(
                    general_buying= self.general_buying, 
                    amount=self.amount,
                    price=self.price,
                    description=note,
                    created_at=self.created_at,
                )
                
                self.token = generalInner.token  # Set the payment token
                self.pakage.add_to_stock(self.amount)

          super().save(*args, **kwargs)

    
        def delete(self, *args, **kwargs):
            # Find the corresponding GeneralPayment using the payment_token
            try:
                general_payment = GeneralInner.objects.get(token=self.token)
                general_payment.delete()  # Delete the GeneralPayment record

                self.pakage.remove_from_stock(self.amount)
      
            except GeneralInner.DoesNotExist:
                pass  
            super().delete(*args, **kwargs)
        





class Material(models.Model):
    product_name = models.TextField()
    stock = models.DecimalField(default=0, max_digits=10, decimal_places=2 ,validators=[MinValueValidator(0)])  # New stock field
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    adjustment = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        # Adjust stock before saving
        if self.adjustment > 0:
            self.stock += self.adjustment
            self.adjustment = 0  # Reset adjustment after applying it
        super().save(*args, **kwargs)

    def add_to_stock(self, amount):
        
        self.stock += amount
        self.save()

    def remove_from_stock(self, amount):
        self.stock -= amount
        self.save()

    def setPrice(self , price):
         self.price = price
         self.save()
















class RawMaterials(models.Model):
    product_name = models.TextField()
    Materials = models.ForeignKey(Material, related_name="select_Materials_to_set", on_delete=models.CASCADE)
    WaistPercentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], default=0)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    adjustment = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field

    def __str__(self):
        return self.product_name
    

    def save(self, *args, **kwargs):
        # Set the 'name' field before saving
        self.stock = self.adjustment + self.stock
        self.adjustment = 0
        super().save(*args, **kwargs)

    def add_to_stock(self , amount):
       
        self.stock += amount
        self.save()

    def remove_from_stock(self , amount):
       
        self.stock -= amount
        self.save()





    def Modify_persentge_increse(self,amount):
         modified = amount - amount*self.WaistPercentage/100
         
        
         self.Materials.add_to_stock(modified)

         self.save()


    def Modify_persentge_dincrese(self,amount):
            modified = amount + amount*self.WaistPercentage/100
 
         
            self.Materials.remove_from_stock(modified)
         
            self.save()
            


class RawmaterialsInner(models.Model):
    general_buying = models.ForeignKey(GeneralBuying, on_delete=models.CASCADE, related_name='RawMaterials_to_buy')
    RawMaterials = models.ForeignKey(RawMaterials, related_name="select_RawMaterials_to_buy", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=255, blank=True, null=True )
    token = models.UUIDField(editable=False, unique=True , null=True)  # Unique payment token
    created_at = models.DateField(default=timezone.now)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
          return f"{self.general_buying} - {self.RawMaterials} - {self.amount}  {self.price}"

    



    def save(self, *args, **kwargs):
          if not self.created_at:
                 self.created_at = timezone.now().date()
          self.total = self.amount * self.price
          note = f"{self.RawMaterials.product_name}  : {self.note}"
          if not self.pk:  # Check if this is a new record
                super().save(*args, **kwargs) 
                 # Save the EmployeePayment first
                

                generalInner = GeneralInner.objects.create(
                    general_buying= self.general_buying, 
                    amount=self.amount,
                    price=self.price,
                    description=note,
           
                    created_at=self.created_at,       
                )
                
                self.token = generalInner.token  # Set the payment token
                self.RawMaterials.Modify_persentge_increse(self.amount)
                self.RawMaterials.Materials.setPrice(self.price)
          super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
            # Find the corresponding GeneralPayment using the payment_token
            try:
                general_payment = GeneralInner.objects.get(token=self.token)
                general_payment.delete()  # Delete the GeneralPayment record

                self.RawMaterials.Modify_persentge_dincrese(self.amount)
      
            except GeneralInner.DoesNotExist:
                pass  # If no corresponding GeneralPayment is found, continue with the deletion

            super().delete(*args, **kwargs)
        





class FactoryMaterials(models.Model):
    product_name = models.TextField()
    Materials = models.ForeignKey(Material, related_name="select_Materials_to_set_factory", on_delete=models.CASCADE)
    WaistPercentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], default=0)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    adjustment = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field

    def __str__(self):
        return self.product_name
    

    def save(self, *args, **kwargs):
        # Set the 'name' field before saving
        self.stock = self.adjustment + self.stock
        self.adjustment = 0
        super().save(*args, **kwargs)

    
    def add_to_stock(self , amount):
       
        self.stock += amount
        self.save()

    def remove_from_stock(self , amount):
       
        self.stock -= amount
        self.save()



    def Modify_persentge_increse(self,amount):
         modified = amount - amount*self.WaistPercentage/100
         self.stock += modified
         self.Materials.add_to_stock(modified)
         self.save()


    def Modify_persentge_dincrese(self,amount):
            modified = amount + amount*self.WaistPercentage/100
            self.stock -= modified
            self.Materials.remove_from_stock(modified)
            self.save()
            










class FacoryMaterialsInner(models.Model):
    general_buying = models.ForeignKey(GeneralBuying, on_delete=models.CASCADE, related_name='inner_FacoryMaterialsInner')
    RawMaterials = models.ForeignKey(FactoryMaterials, related_name="select_FactoryMaterials_to_buy", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=255, blank=True, null=True )
    token = models.UUIDField(editable=False, unique=True , null=True)  # Unique payment token
    created_at = models.DateField(default=timezone.now)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)


    def save(self, *args, **kwargs):
          if not self.created_at:
                 self.created_at = timezone.now().date()
          self.total = self.amount * self.price
          notee = f"{self.RawMaterials.product_name}"
          if not self.pk:  # Check if this is a new record
                super().save(*args, **kwargs) 
           
                

                generalInner = GeneralInner.objects.create(
                    general_buying= self.general_buying, 
                    amount=self.amount,
                    price=self.price,
                    description=notee,
                    note=self.note,
                    created_at=self.created_at,       
                )
                
                self.token = generalInner.token  # Set the payment token
                self.RawMaterials.Modify_persentge_increse(self.amount)
                self.RawMaterials.Materials.setPrice(self.price)


          super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
            # Find the corresponding GeneralPayment using the payment_token
            try:
                general_payment = GeneralInner.objects.get(token=self.token)
                general_payment.delete()  # Delete the GeneralPayment record

                self.RawMaterials.Modify_persentge_dincrese(self.amount)
      
            except GeneralInner.DoesNotExist:
                pass  # If no corresponding GeneralPayment is found, continue with the deletion

            super().delete(*args, **kwargs)
        








class ProductMaterial(models.Model):
    product = models.ForeignKey(ProductHam, on_delete=models.CASCADE, related_name='ProductMaterial_toset')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])  # Quantity of the material used

    class Meta:
        unique_together = ('product', 'material')  # Ensure a product can have only one entry for each material

    def __str__(self):
        return f"{self.product.product_name} - {self.material.product_name} ({self.quantity})"
    


    def save(self, *args, **kwargs):
        # Update the price based on the total cost every time the product is saved
        self.product.save()
        super().save(*args, **kwargs)



class Recipe(models.Model):
    product_ham = models.ForeignKey(ProductHam, on_delete=models.CASCADE, related_name='recipes')
    material = models.ForeignKey(Material, on_delete=models.CASCADE , related_name="choose_recipe_meterial")
    quantity_needed = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    prepare = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])




    def __str__(self):
        return f'{self.quantity_needed} of {self.material.product_name} for {self.product_ham.product_name}'

    def decrease_from_stock(self):
        """
        Calculate how much material is needed based on the amount being prepared,
        and decrease the stock accordingly.
        """

        print("function has ween caled")
      
        # Calculate the required amount for the current preparation
        wanted_amount = self.product_ham.prepare * self.quantity_needed / self.product_ham.top
        
        # Check if there's enough stock to decrease
        if wanted_amount <= self.material.stock:
            self.material.remove_from_stock(wanted_amount)  # Decrease stock
        else:
            raise ValueError(f"Not enough stock of {self.material.product_name}.")
        




class Assets(models.Model):
    name = models.TextField()
    stock = models.DecimalField(default=0, max_digits=10, decimal_places=2 ,validators=[MinValueValidator(0)])  # New stock field
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    adjustment = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field
    image = models.ImageField(upload_to='assets/', blank=True, null=True)  # Image field for profile image

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Adjust stock before saving
        if self.adjustment > 0:
            self.stock += self.adjustment
            self.adjustment = 0  # Reset adjustment after applying it
        super().save(*args, **kwargs)

    def add_to_stock(self, amount):
        
        self.stock += amount
        self.save()

    def remove_from_stock(self, amount):
        self.stock -= amount
        self.save()

    def setPrice(self , price):
         self.price = price
         self.save()




class AssetsInner(models.Model):
        general_buying = models.ForeignKey(GeneralBuying, on_delete=models.CASCADE, related_name='inner_Assets')
        product = models.ForeignKey(Assets, related_name="select_Assets_to_buy", on_delete=models.CASCADE)
        amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=0)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        note = models.CharField(max_length=255, blank=True, null=True )
        token = models.UUIDField(editable=False, unique=True , null=True)  # Unique payment token
        created_at = models.DateField(default=timezone.now)
        total = models.DecimalField(default=0, max_digits=10, decimal_places=2)


        def save(self, *args, **kwargs):
          if not self.created_at:
                 self.created_at = timezone.now().date()
          self.total = self.amount * self.price

        
          note = f"{self.product}  : {self.note}"
 


          if not self.pk:  # Check if this is a new record
                super().save(*args, **kwargs) 
                 # Save the EmployeePayment first
                

                generalInner = GeneralInner.objects.create(
                    general_buying= self.general_buying, 
                    amount=self.amount,
                    price=self.price,
                    description=note,
                    created_at=self.created_at,
                )
                
                self.token = generalInner.token  # Set the payment token
                self.product.add_to_stock(self.amount)

          super().save(*args, **kwargs)

    
        def delete(self, *args, **kwargs):
            # Find the corresponding GeneralPayment using the payment_token
            try:
                general_payment = GeneralInner.objects.get(token=self.token)
                general_payment.delete()  # Delete the GeneralPayment record

                self.product.remove_from_stock(self.amount)
      
            except GeneralInner.DoesNotExist:
                pass  
            super().delete(*args, **kwargs)
        



class SpendesType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    Name_En = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=1)


    def __str__(self):
        return self.name




class Spendes(models.Model):
        general_buying = models.ForeignKey(GeneralBuying, on_delete=models.CASCADE, related_name='inner_Spendes')
        amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(999999)] ,default=1)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        note = models.CharField(max_length=255, blank=True, null=True )
        token = models.UUIDField(editable=False, unique=True , null=True)  # Unique payment token
        created_at = models.DateField(default=timezone.now)
        total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        buying_type = models.ForeignKey(SpendesType, on_delete=models.CASCADE)


        def save(self, *args, **kwargs):
          if not self.created_at:
                 self.created_at = timezone.now().date()
          self.total = self.amount * self.price

        
          note = f"{self.note }"
 


          if not self.pk:  # Check if this is a new record
                super().save(*args, **kwargs) 
                 # Save the EmployeePayment first
                

                generalInner = GeneralInner.objects.create(
                    general_buying= self.general_buying, 
                    amount=self.amount,
                    price=self.price,
                    description=note,
                    created_at=self.created_at,
                )
                
                self.token = generalInner.token  # Set the payment token

          super().save(*args, **kwargs)

    
        def delete(self, *args, **kwargs):
            # Find the corresponding GeneralPayment using the payment_token
            try:
                general_payment = GeneralInner.objects.get(token=self.token)
                general_payment.delete()  # Delete the GeneralPayment record

               
      
            except GeneralInner.DoesNotExist:
                pass  
            super().delete(*args, **kwargs)
        

