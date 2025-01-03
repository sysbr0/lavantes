from django.contrib import admin
from .models import MoneySource , GeneralPayment , CustomerPaymentTl , CustomerPaymentUsd , EmployePayment , sorcePyment
admin.site.register(MoneySource)
admin.site.register(GeneralPayment)
admin.site.register(CustomerPaymentTl)
admin.site.register(CustomerPaymentUsd)
admin.site.register(EmployePayment)
admin.site.register(sorcePyment)


