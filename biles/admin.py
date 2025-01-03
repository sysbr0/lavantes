from django.contrib import admin
from .models import Package , Jar , ProductHam , MainProduct , UdsBills  , UdsBill_inner  ,TrBills , TrBill_inner, Purchase , Jar_compine , Jar_off # ,UdsBill , yh  , Purchase

admin.site.register(Package)
admin.site.register(Jar)
admin.site.register(ProductHam)
admin.site.register(MainProduct)
admin.site.register(UdsBill_inner)
#admin.site.register(UdsBill)

#admin.site.register(yh)
admin.site.register(UdsBills)
admin.site.register(TrBills)
admin.site.register(TrBill_inner)
admin.site.register(Purchase)
admin.site.register(Jar_compine)
admin.site.register(Jar_off) 



# Register your models here.
