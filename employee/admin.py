from django.contrib import admin
from .models import Employee , Attendance, Salary , EmployeePayment
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Salary)
admin.site.register(EmployeePayment)
# Register your models here.
