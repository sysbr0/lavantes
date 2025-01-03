from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Costomers
from django.utils import timezone
from django.urls import reverse
import json

from decimal import Decimal


from django.utils.timezone import now

class Package(models.Model):
    id = models.IntegerField(primary_key=True) 
    package_name = models.TextField()
    package_arabic = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_package')
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    adjustment = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field
    image = models.ImageField(upload_to='Package/', blank=True, null=True)  # Image field for profile image
    changablty  =  models.BooleanField(default=False)

    def __str__(self):
        return self.package_name
    

    def save(self, *args, **kwargs):
        # Set the 'name' field before saving
        self.stock = self.adjustment + self.stock
        self.adjustment = 0
        super().save(*args, **kwargs)


    def add_to_stock(self , amount):
        if self.changablty:
            self.stock += amount
            self.save()

    def remove_from_stock(self , amount):
        if self.changablty:
            self.stock -= amount
            self.save()














class Jar_off(models.Model):
    jar_name = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_jarof')
    stock = models.IntegerField(default=0)  # New stock field
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    adjustment = models.IntegerField(default=0)  # New stock field
    image = models.ImageField(upload_to='jar_off/', blank=True, null=True)  # Image field for profile image
    changablty  =  models.BooleanField(default=False)

    




    def __str__(self):
        return self.jar_name
    

    def save(self, *args, **kwargs):
        # Set the 'name' field before saving
        self.stock = self.adjustment + self.stock
        self.adjustment = 0
        super().save(*args, **kwargs)



    
    def add_to_stock(self , amount):
        if self.changablty:
            self.stock += amount
            self.save()

    def remove_from_stock(self , amount):
        if self.changablty:
            self.stock -= amount

            print("done ")
            self.save()



class Jar(models.Model):
    jar_name = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_jar')
    image = models.URLField(blank=True, null=True)
    stock = models.IntegerField(default=0)  # New stock field
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    adjustment = models.IntegerField(default=0)  # New stock field
    image = models.ImageField(upload_to='jars/', blank=True, null=True)  # Image field for profile image
    changablty  =  models.BooleanField(default=False)



    def __str__(self):
        return self.jar_name
    

    def save(self, *args, **kwargs):
        # Set the 'name' field before saving
        self.stock = self.adjustment + self.stock
        self.adjustment = 0
        super().save(*args, **kwargs)

    def add_to_stock(self , amount):
         if self.changablty:
                self.stock += amount
                self.save()

    def remove_from_stock(self , amount):
         if self.changablty:
                self.stock -= amount
                self.save()

    




class Jar_compine(models.Model):
    name = models.TextField()
    jar = models.ForeignKey(Jar, related_name="select_jar_to_compine", on_delete=models.CASCADE)
    towich = models.ForeignKey(Jar_off, related_name="select_jar_off_to_compine", on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_compine')
    image = models.ImageField(upload_to='jar_compaine/', blank=True, null=True)  # Image field for profile image

    def __str__(self):
         return f"{self.jar.jar_name}  {self.towich.jar_name}  "
    


    def add_to_stock(self , amount):
        self.towich.add_to_stock(amount)
     

       

    def remove_from_stock(self , amount):
         
         print(" removing twich")
         self.towich.remove_from_stock(amount)
        


    




class ProductHam(models.Model):
    product_name = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_product_ham')
    top = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])
    adjustment = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # New stock field
    image = models.ImageField(upload_to='ProductHam/', blank=True, null=True)  # Image field for profile image
    prepare = models.DecimalField(default=0,max_digits=10, decimal_places=2, validators=[MinValueValidator (0)])

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        # Adjust stock based on adjustment
        if self.adjustment > 0:
            self.stock += self.adjustment
            self.adjustment = 0  # Reset adjustment after applying it

        # If prepare field is greater than 0, adjust stock based on recipes
        if self.prepare > 0 and self.top>0:
            from main.models import Recipe
            recipes = Recipe.objects.filter(product_ham=self)
            
            # Loop through each recipe to decrease the stock for each material
            for recipe in recipes:

                value = recipe.quantity_needed*self.prepare/self.top
                recipe.material.remove_from_stock(value)

                
                  # Decrease material stock
            
            # Reset prepare field to 0 after processing
            self.stock +=self.prepare
            self.prepare = 0


        super().save(*args, **kwargs)  # Call the parent save method
        



class MainProduct(models.Model):
    product_name = models.TextField()
    product_type = models.TextField()
    product_ham = models.ForeignKey(ProductHam, related_name="select_ham", on_delete=models.CASCADE)
    Jar_compine = models.ForeignKey(Jar_compine, related_name="select_to_compaine", on_delete=models.CASCADE , default=1) 
    jar = models.ForeignKey(Jar, related_name="select_jar", on_delete=models.CASCADE)
    package = models.ForeignKey(Package, related_name="select_package", on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_main_product')
    image = models.URLField(blank=True, null=True)
    net_weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    top_weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    amount_inside = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    qr = models.IntegerField(primary_key=True)
    CustomName = models.TextField(blank=True, null=True)
    IsCustom = models.BooleanField(default=False)
    name = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['product_ham', 'net_weight']  # Default ordering by primary key
    def get_absolute_url(self):
        return reverse('fatch_Product', kwargs={'id': self.pk})




    def __str__(self):
        return  self.name
    def net(self):
        return self.net_weight * self.amount_inside/100
    def top(self):
        return self.top_weight * self.amount_inside/100
    
    def save(self, *args, **kwargs):
        # Set the 'name' field before saving
        if self.IsCustom:
            self.name = self.CustomName
            super().save(*args, **kwargs)  # Call the parent save method
        else:
            self.name = f"{self.package.package_arabic} {self.product_name} {self.product_type} الوزن الصافي {self.net_weight} الشد {self.amount_inside}  الرمز [ {self.qr} ]"

        
        super(MainProduct, self).save(*args, **kwargs)



    def refresh_stock_out(self, amount):
            
            print("resresh stok startes")

            jar = Jar.objects.get(id=self.jar.pk)
           
            jarcom = Jar_compine.objects.get(id=self.Jar_compine.pk)
            package = Package.objects.get(id=self.package.id)
            product_ham = ProductHam.objects.get(id=self.product_ham.pk)

            #jar and twich 
            jarcom.remove_from_stock(amount * self.amount_inside)
            package.remove_from_stock(amount)
         
            product_ham.stock -= amount * self.amount_inside * self.net_weight / 1000
            product_ham.save()

            jar.remove_from_stock(amount * self.amount_inside)
            print("taking")
            print(jar.stock)

            print("pakage")
            print(package.stock)

            print("ham ")
            print(product_ham.stock)





                
    def refresh_stock_in(self, amount):
            jar = Jar.objects.get(id=self.jar.pk)
            jarcom = Jar_compine.objects.get(id=self.Jar_compine.pk)
            package = Package.objects.get(id=self.package.id)
            product_ham = ProductHam.objects.get(id=self.product_ham.pk)

            # Check if there's enough stock before updating
        
            jar.add_to_stock(amount * self.amount_inside)
            jarcom.add_to_stock(amount * self.amount_inside)
    
     
            package.stock += amount
            package.save()
            product_ham.stock += amount * self.amount_inside * self.net_weight / 1000
            product_ham.save()

            print("returing ")

            print(jar.stock)

            print("pakage")
            print(package.stock)

            print("ham ")
            print(product_ham.stock)







    def refrshing_all_remove(self , amount):
     pass


    def refrshing_all_return(self , amount):
        amount_inside_it = amount*self.amount_inside
        self.Jar_compine.jar.add_to_stock(amount_inside_it)
        self.package.add_to_stock(amount)





        
                
         
 

class UdsBills(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_uds_bills')
    customer = models.ForeignKey(Costomers, on_delete=models.CASCADE, related_name='uds_bills_customers')
    note = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(default=now)
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    net = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    top = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    done  =  models.BooleanField(default=False)



    def __str__(self):
         return f"فاتورة للسيد {self.customer.name} رقم الفاتورة {self.id} "
    
    



    def calculate_total(self):
        total = sum(inner.calculate() for inner in self.select_UdsBill_inner.all())
        self.price = total
        self.save()

     
    def calculate_total_net(self):
        total = sum(inner.net() for inner in self.select_UdsBill_inner.all())
        self.net = total
        self.save()

    def calculate_total_top(self):
        total = sum(inner.top() for inner in self.select_UdsBill_inner.all())
        self.top = total
        self.save()

    

    




    def costomer_name(self):
        return self.customer.name



    def save(self, *args, **kwargs):
         if not self.created_at:
              self.created_at = timezone.now().date()


         self.customer.calculate_balance_usd()
         super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now().date()

        super().save(*args, **kwargs)


        if self.done:
            inner_records = UdsBill_inner.objects.filter(uds_bill=self)

            # Refresh the stock for all the related main products
            for inner in inner_records:
                if not  inner.stock_out:
                    print(inner.stock_out)
                    inner.main_product.refresh_stock_out(inner.amount)
                    inner.stock_out = True
                    inner.save()


    def costomer_tex(self):
        return self.customer.tex


    

    def costomer_number(self):
        return self.customer.number
    
    def costomer_company(self):
        return self.customer.company
    


    def costomer_address(self):
        return self.customer.address
    


    def delete(self, *args, **kwargs):

         if self.done:
            inner_records = UdsBill_inner.objects.filter(uds_bill=self)

            # Refresh the stock for all the related main products
            for inner in inner_records:
                if   inner.stock_out:
                    print(inner.stock_out)
                    inner.main_product.refresh_stock_in(inner.amount)
                   

    
    
    
    





class UdsBill_inner(models.Model):
      id = models.BigAutoField(primary_key=True)

      created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_UdsBill_inner')
      uds_bill = models.ForeignKey(UdsBills, on_delete=models.CASCADE, related_name="select_UdsBill_inner")
      main_product = models.ForeignKey(MainProduct, related_name="select_MainProduct", on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0), MaxValueValidator(999999)] )
      price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0), MaxValueValidator(999999)])
      note = models.TextField(blank=True, null=True)
      created_at = models.DateField(auto_now_add=True)
      stock_out =  models.BooleanField(default=False)
    
    
      def __str__(self):
        return f"{self.main_product} amount {self.amount} price {self.price} "
 

      def calculate(self):
        return self.amount * self.price
      
      def net(self):
          return self.amount *self.main_product.amount_inside*self.main_product.net_weight/1000
      
      def get_name(self):
          return self.main_product.name
      
          
      def top(self):
          return self.amount *self.main_product.amount_inside*self.main_product.top_weight/1000
      


      def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        
        self.uds_bill.calculate_total()
        self.uds_bill.calculate_total_net()
        self.uds_bill.calculate_total_top()

      def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.uds_bill.calculate_total()
        self.uds_bill.calculate_total_net()
        self.uds_bill.calculate_total_top()

      def get_Qr(self):
       return self.main_product.qr









class TrBills(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_Tr_bills')
    customer = models.ForeignKey(Costomers, on_delete=models.CASCADE, related_name='Tr_bills_customers')
    note = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=now)
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    net = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    top = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    done  =  models.BooleanField(default=False)
    

    def __str__(self):
         return f"فاتورة للسيد {self.customer.name} رقم الفاتورة {self.id} "
    
    



    def calculate_total(self):
        total = sum(inner.calculate() for inner in self.select_TrBill_inner.all())
        self.price = total
        self.save()

     
    def calculate_total_net(self):
        total = sum(inner.net() for inner in self.select_TrBill_inner.all())
        self.net = total
        self.save()

    def calculate_total_top(self):
        total = sum(inner.top() for inner in self.select_TrBill_inner.all())
        self.top = total
        self.save()

    

    




    def costomer_name(self):
        return self.customer.name



    def save(self, *args, **kwargs):
        # Ensure created_at is populated
        if not self.created_at:
            self.created_at = timezone.now().date()

        self.customer.calculate_balance_tl()
        
        # Call the parent save method
        super().save(*args, **kwargs)
        
        # Check if done and handle stock_out logic
        if self.done:
            inner_records = TrBill_inner.objects.filter(Tr_bill=self)

            # Refresh the stock for all the related main products
            for inner in inner_records:
                if not  inner.stock_out:
                    print(inner.stock_out)
                    inner.main_product.refresh_stock_out(inner.amount)
                    inner.stock_out = True
                    inner.save()



    def costomer_tex(self):
        return self.customer.tex


    

    def costomer_number(self):
        return self.customer.number
    
    def costomer_company(self):
        return self.customer.company
    


    def costomer_address(self):
        return self.customer.address
    
   
    def delete(self, *args, **kwargs):

         if self.done:
            inner_records = TrBill_inner.objects.filter(Tr_bill=self)

            # Refresh the stock for all the related main products
            for inner in inner_records:
                if   inner.stock_out:
                    print(inner.stock_out)
                    inner.main_product.refresh_stock_in(inner.amount)
                   




         super().delete(*args, **kwargs)
 
    
       



class TrBill_inner(models.Model):
      id = models.BigAutoField(primary_key=True)

      created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_TrBill_inner')
      Tr_bill = models.ForeignKey(TrBills, on_delete=models.CASCADE, related_name="select_TrBill_inner")
      main_product = models.ForeignKey(MainProduct, related_name="select_MainProduct_tr", on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0), MaxValueValidator(999999)] )
      price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0), MaxValueValidator(999999)])
      created_at = models.DateField(auto_now_add=True)
      note = models.TextField(blank=True, null=True)
      stock_out =  models.BooleanField(default=False)
    
      def __str__(self):
        return f"{self.main_product} amount {self.amount} price {self.price} "
 

      def calculate(self):
        return self.amount * self.price
      
      def net(self):
          return self.amount *self.main_product.amount_inside*self.main_product.net_weight/1000
      
      def get_name(self):
          return self.main_product.name
      
          
      def top(self):
          return self.amount *self.main_product.amount_inside*self.main_product.top_weight/1000
      


      def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
       
   
        self.Tr_bill.calculate_total()
        self.Tr_bill.calculate_total_net()
        self.Tr_bill.calculate_total_top()

      



    

      def delete(self, *args, **kwargs):
   
            
        
        self.Tr_bill.calculate_total()
        self.Tr_bill.calculate_total_net()
        self.Tr_bill.calculate_total_top()

        super().delete(*args, **kwargs)

      def get_Qr(self):
       return self.main_product.qr





class Purchase(models.Model):
    PRODUCT_CHOICES = [
        ('jar', 'Jar'),
        ('package', 'Package'),
        ('ham', 'ProductHam'),
    ]

    product_type = models.CharField(max_length=20, choices=PRODUCT_CHOICES)
    product_id = models.PositiveIntegerField()  # This will store the ID of the Jar, Package, or ProductHam
    quantity = models.IntegerField(validators=[MinValueValidator(1)])  # Amount purchased
    purchase_date = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Reduce stock based on the product type
        if self.product_type == 'jar':
            jar = Jar.objects.get(id=self.product_id)
            jar.stock = jar.stock - self.quantity
            jar.save()
        elif self.product_type == 'package':
            package = Package.objects.get(id=self.product_id)
            package.stock = package.stock - self.quantity
            package.save()
        elif self.product_type == 'ham':
            ham = ProductHam.objects.get(id=self.product_id)
            ham.stock = ham.stock - self.quantity
            ham.save()

    def __str__(self):
        return f'{self.buyer} bought {self.quantity} {self.product_type}(s)'
