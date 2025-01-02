from django.db import models
from django.conf import settings
from datetime import date, timedelta

from django.utils import timezone
import uuid
# Create your models here.



class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100 ,blank=True, null=True )
    age = models.IntegerField(blank=True, null=True)
    tc = models.CharField(max_length=11, blank=True, null=True, unique=True)  # Use CharField for TC    title = models.CharField(max_length=100 , blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.IntegerField(null=True , blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)  # Add this line
    state = models.BooleanField(default=True)  # True for active, False for inactive
    E_salary = models.IntegerField(default=0 )
    balance = models.IntegerField(blank=True, null=True)
    is_working = models.BooleanField(default=True)  # True for active, False for inactive
    phone = models.CharField(max_length=10, blank=True, null=True, unique=True)  # Use CharField for TC    title = models.CharField(max_length=100 , blank=True, null=True)
    phone_2 = models.CharField(max_length=10, blank=True, null=True, unique=True) 

   


    def update_state(self):
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_attendances = Attendance.objects.filter(employee=self, date__gte=thirty_days_ago)
        if recent_attendances.exists():
            self.state = True  # Employee has attended within the last 30 days
        else:
            self.state = False  # Employee has not attended within the last 30 days

        self.save()
    def save(self, *args, **kwargs):
        if not self.pk:  # Only set created_by on creation, not on update
            self.created_by = kwargs.pop('created_by', None)  # Pop the created_by user from kwargs if provided
        super(Employee, self).save(*args, **kwargs)


    def __str__(self):
        return f" {self.name } "
    

    def calculate_balance(self):
        total_payments = EmployeePayment.objects.filter(employee=self).aggregate(total=models.Sum('amount'))['total'] or 0
        total_salaries = self.calculate_total_salaries()
        balance = total_payments - total_salaries
        return balance

    def calculate_total_salaries(self):
        total_salaries = 0
        attendances = Attendance.objects.filter(employee=self)

        for attendance in attendances:
            salary = Salary.objects.filter(employee=self, effective_date__lte=attendance.date).order_by('-effective_date').first()
            if salary:
                total_salaries += salary.amount

        return total_salaries
    


    def calculate_salary_details(self):
        salary_details = []
        attendances = Attendance.objects.filter(employee=self).order_by('date')
        current_salary = None
        total_salary = 0
        day_count = 0

        for attendance in attendances:
            salary = Salary.objects.filter(employee=self, effective_date__lte=attendance.date).order_by('-effective_date').first()
            if salary and (not current_salary or salary.effective_date > current_salary.effective_date):
                if current_salary:
                    salary_details.append({
                        'start_date': start_date,
                        'end_date': attendance.date - timedelta(days=1),
                        'days': day_count,
                        'daily_salary': current_salary.amount,
                        'total_salary': day_count * current_salary.amount
                    })
                    total_salary += day_count * current_salary.amount

                current_salary = salary
                start_date = attendance.date
                day_count = 0

            day_count += 1

        if current_salary:
            salary_details.append({
                'start_date': start_date,
                'end_date': attendances.last().date,
                'days': day_count,
                'daily_salary': current_salary.amount,
                'total_salary': day_count * current_salary.amount
            })
            total_salary += day_count * current_salary.amount

        return salary_details, total_salary




    


  

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_attandec')

    status = models.CharField(max_length=10 , blank=True, null=True)  # e.g., 'Present', 'Absent'
    ispyed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.employee.name} - {self.date}'
    
    def employe(self):
        return f" {self.employee.name } "
    

    def get_employee_name(self):
        return self.employee.name if self.employee else "Unknown Employee"
    

    def created_by_admin(self):
        return self.created_by.full_name


    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created
            # Check if there is already an attendance record for this employee on the same date
            existing_attendance = Attendance.objects.filter(employee=self.employee, date=self.date).first()
            if existing_attendance:
                # If an attendance record exists, update it instead of creating a new one
                existing_attendance.status = self.status
                existing_attendance.save()
                return existing_attendance
            


            
            
        
        # If no existing attendance record, proceed with normal save
        super().save(*args, **kwargs)
        
        # Update the employee state after saving attendance
        self.employee.update_state()



        all_attendances_paid = Attendance.objects.filter(employee=self.employee, ispyed=False).exists()
        if not all_attendances_paid:
            self.employee.state = False
            self.employee.save()
        return self
    


 
    def employe_id(self):
     return self.employee.id 
    


class Salary(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField(default=timezone.now)  # Date when this salary amount becomes effective

    def __str__(self):
        return f"{self.employee.name} - {self.amount} from {self.effective_date}"
    


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.employee.E_salary = self.amount
        self.employee.save()
    
    

  



from django.utils import timezone


class EmployeePayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    note = models.TextField(default="None")  # Note about the payment
    payment_token = models.UUIDField(editable=False, unique=True , null=True)  # Unique payment token

 

    def __str__(self):
        return f"Payment of {self.amount} to {self.employee.name} on {self.date} "
 
    
