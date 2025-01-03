

# Register your models here.

from django.contrib import admin
from .models import Message , Product_imges , Swapper_Imges , Address , MessageLog

admin.site.register(Message)
admin.site.register(Product_imges)
admin.site.register(Swapper_Imges)
admin.site.register(Address)  # Register the model here
admin.site.register(MessageLog)  # Register the model here

