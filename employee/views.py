

# views.py
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import calendar
from .models import Attendance, Employee , Salary , EmployeePayment
import csv
from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404 , redirect

from datetime import datetime
from datetime import date
from .forms import EmployeeForm ,  TCForm , MarkPaidForm  , SalaryForm , EmployeePaymentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.db import transaction
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.utils import timezone
from calendar import Calendar
from django.urls import reverse
from users.forms import LogingForm
from datetime import datetime, timedelta
import google.generativeai as genai
import os

from django.views.decorators.csrf import csrf_exempt


import plotly.express as px
import plotly.graph_objs as go
import plotly.utils


Gemini_API = os.getenv('Gemini_API')

genai.configure(api_key=Gemini_API)

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="This is a company management system.",
)




def admin_chat(request):
    name = request.user.email if request.user.is_authenticated else None



    # Retrieve employee and attendance records
    employee = Employee.objects.all()
  
    attendance_records = Attendance.objects.all()
    

    # Create arrays for employee and attendance information
    employee_info = [ {
        "name": record.name,
        "age": record.age,
        "position": record.position,
        "tc": record.tc,
        "title": record.title,
        "state": record.state,
    }
     for record in employee
    ]

    attendance_info = [
        {
            "employee": record.employee,
            "date": record.date,
            "status": record.status,
            "is_paid": record.ispyed,
        }
        for record in attendance_records
    ]

    # Initialize chat session with predefined messages for context
    chat_history = [


        {"role": "user", "parts": [f" مرحبا ساقوم بارسال بعض البيانات عن العاملين لدي ولدي ايضا جدول  يعرض  ايام الجضور لكل شخص وهنالك  خيار يعرض اذا كان اليوم مدوفع او لا  اجب بللغة العربية حصرا "]},


        {"role": "model", "parts": [f"مرحبا ,  بالطبع سؤجيب بالغة لعربية ، كيف يمكنني مساعدتك اليوم  ?"]},
        {"role": "user", "parts": ["اريد ان اعرف كم يوم لي في العمل سواء ايام مدفوقة او ايام غير مدفوعة  لكن احرص على ان البيانات التي سترسلها ستكون عبارة عن تنسيق html ولا تنسى التنسيق فهو مهم جداا  css?"]},
        {"role": "model", "parts": ["هل يمكنك ارسال المعلومات او البيانات "]},
    ]

    for record in attendance_info:
        chat_history.append(
            {"role": "user", "parts": [f"التاريخ: {record['date']}, الحالة : {record['status']}, حالة الدفع : {record['is_paid']}  العامل هو {record['employee']}"]}
        )

    for record in employee_info:
        chat_history.append(
            {"role": "user", "parts": [f"اسم العاملة : {record['name']}, الاسم بلانجليزية : {record['title']}, المعرف  : {record['tc']}"]}
        )

    

    chat_session = model.start_chat(history=chat_history)

    if request.method == 'POST':
        user_input = request.POST.get('message', '')

        # Send the user input to the model and get the response
        response = chat_session.send_message(user_input)
        model_response = response.text

        # Append to history
        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})

        return JsonResponse({'response': model_response})

    context = {
        'employee_info': employee_info,
        'attendance_info': attendance_info,
        "name" :name,
    }

    return render(request, 'chat.html', context)






def chat_view(request, id):
    # Retrieve employee and attendance records
    employee = get_object_or_404(Employee, id=id)

    
    attendance_records = Attendance.objects.filter(employee=employee)
    pyment = EmployeePayment.objects.filter(employee=employee)
    salary = Salary.objects.filter(employee=employee)


    # Create arrays for employee and attendance information
    employee_info = {
        "name": employee.name,
        "age": employee.age,
        "position": employee.position,
        "tc": employee.tc,
        "title": employee.title,
        "state": employee.state,
    }
    name = employee_info['name']



    attendance_info = [

        {
            
            "date": record.date,
            "status": record.status,
            "is_paid": record.ispyed,
        }
        for record in attendance_records
    ]


    pyment_info = [

        {
            
            "date": record.date,
            "amount": record.amount,
            "note": record.note,
        }
        for record in pyment
    ]


    salary_info = [

        {
            
            "date": record.effective_date,
            "amount": record.amount,
      
        }
        for record in salary
    ]






    # Initialize chat session with predefined messages for context
    chat_history = [
        {"role": "user", "parts": [f"مرحبا انا اسمي  {employee.name}. رجاءا لا تتحدث الا باللغة العربية انا لا اجيد الإنجليزية "]},
        {"role": "model", "parts": [f"مرحبا  {employee.name},  بالطبع سؤجيب بالغة لعربية ، كيف يمكنني مساعدتك اليوم  ?"]},
        {"role": "user", "parts": ["اريد ان اعرف كم يوم لي في العمل  و كم اخذت من اموال  ?"]},
        {"role": "model", "parts": ["هل يمكنك ارسال المعلومات او البيانات "]},
    ]


    for record in attendance_info:
        chat_history.append(
            {"role": "model", "parts": [f"التاريخ: {record['date']}, الحالة : {record['status']} "]}
        )
    for record in attendance_info:
        chat_history.append(
            {"role": "model", "parts": [f"التاريخ: {record['date']}, الحالة : {record['status']}  ايام الحضور مضروبة بالمعاش اليومي الذي تم تحديده في اخر فترة على سبيل المثال الاسبوع السابق كان معاشي مبلغ معين وتم رفعه بمبلغ معين فالايام السابقة تبقى على ما هي والايام الجديد تضرب باليومية الجديدة سارسل لك ايضا الدفعات ويومياتي حسب التاريخ "]}
        )

    for record in pyment_info:
        chat_history.append(
            {"role": "model", "parts": [f"التاريخ: {record['date']}, المبلغ  : {record['amount']}   الملاحظة  {record['note']} "]}
        )

    for record in salary_info:
        chat_history.append(
            {"role": "model", "parts": [f"التاريخ: {record['date']}, المبلغ  : {record['amount']}  هذه هي قيمة معاشي بناء على التاريخ  "]}
        )


    chat_session = model.start_chat(history=chat_history)

    if request.method == 'POST':
        user_input = request.POST.get('message', '')

        # Send the user input to the model and get the response
        response = chat_session.send_message(user_input)
        model_response = response.text

        # Append to history
        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})

        return JsonResponse({'response': model_response})

    context = {
        'employee_info': employee_info,
        'attendance_info': attendance_info,
        "name" : name
    }

    return render(request, 'chat.html', context)



def download_employee_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')

   
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Id','Name', 'Position', 'Age', 'TC', 'Created At', 'Created By', 'Title', 'State'])

    # Write the data rows
    employees = Employee.objects.all()
    for employee in employees:
        writer.writerow([
            employee.id,
            employee.name,
            employee.position,
            employee.age,
            employee.tc,
            employee.created_at,
            employee.created_by,
            employee.title,
            employee.state,
        ])

    return response









def download_attendance_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Employee Name', 'Date', 'Created By', 'Status', 'Is Paid'])

    attendances = Attendance.objects.all()
    for attendance in attendances:
        writer.writerow([
            attendance.employee.id,
            attendance.get_employee_name(),
            attendance.date,
            attendance.created_by,  # Assuming AUTH_USER_MODEL has a 'username' field
            attendance.status,
            attendance.ispyed,
        ])

    return response





def calendar_view(request):
    # Get today's date
    now = datetime.now()
    
    # Determine the month and year from query parameters if provided, otherwise use current month and year
    month = request.GET.get('month', now.month)
    year = int(request.GET.get('year', now.year))
    
    # Convert month to integer if it's a string
    try:
        month = int(month)
    except ValueError:
        month = now.month

    # Calculate the previous and next months and years
    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    # Get the calendar month as a list of tuples (day, weekday)
    cal = calendar.monthcalendar(year, month)

    # Context data to pass to the template
    context = {
        'now': now,
        'calendar': cal,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],  # Get month name as string
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    
    return render(request, 'attendance/calendar.html', context)

def attendance_view(request, year, month, day):
    date_string = f'{year}-{month}-{day}'
    formatted_date = date(year, month, day)



        # Retrieve Attendance object or raise 404 if not found
    attendance = Attendance.objects.filter(date =formatted_date )
 

    context = {
        'attendance': attendance,
        'attendance_date': formatted_date,
        'date_string' :date_string
    }

    return render(request, 'attendance/attendance.html', context)



def attendance_view_admin(request, year, month, day):
    date_string = f'{year}-{month}-{day}'
    formatted_date = date(year, month, day)



        # Retrieve Attendance object or raise 404 if not found
    attendance = Attendance.objects.filter(date =formatted_date )
    count_attendance = attendance.count()
 

    context = {
        'attendance': attendance,
        'attendance_date': formatted_date,
        'date_string' :date_string,
        "count_attendance":count_attendance
    }

    return render(request, 'attendance/attandce_admin.html', context)





@login_required
def add_employee(request):
    email = request.user.email if request.user.is_authenticated else None
    print(email)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            if not employee.created_by:  # Ensure not to override if already set
                employee.created_by = request.user.id  # Assuming you want to store the user ID
            employee.save()
            return redirect('employee_list_view')
    else:
        form = EmployeeForm()

    context = {
        'form': form,
        'email': email
    }
    return render(request, 'employe/add.html', context)



@login_required
def employee_list_view(request):
    employees = Employee.objects.all()
    email = request.user.email if request.user.is_authenticated else None
    return render(request, 'employe/list.html', {'employees': employees , 'email':email})




@login_required
def employee_Salary_not_add(request):
    employees = Employee.objects.filter(is_working=True, E_salary=0)
    email = request.user.email if request.user.is_authenticated else None
    return render(request, 'salary/not_add.html', {'employees': employees , 'email':email})



@login_required
def pyment(request):
    today = date.today()
    employes = Employee.objects.all()


    employees = [employee for employee in employes if employee.is_working and employee.calculate_balance() != 0]
    total_balance = sum(employee.calculate_balance() for employee in employees)


    email = request.user.email if request.user.is_authenticated else None
    return render(request, 'pyment/report.html', {'employees': employees , 'email':email , "total":total_balance , "today" :today})


@login_required
def employee_payment_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    
    if request.method == 'POST':
        form = EmployeePaymentForm(request.POST)
        if form.is_valid():
            form.instance.employee = employee  # Set the employee instance
            form.save()
            messages.success(request, 'Payment has been successfully created.')
            return redirect('employee_payment_view', id=id)
        else:
            messages.error(request, 'There was an error with the form submission.')
    else:
        form = EmployeePaymentForm()
    
    last_payments = EmployeePayment.objects.filter(employee=employee).order_by('-date')[:10]

    context = {
        'employee': employee,
        'form': form,
        'last_payments': last_payments,
    }

    return render(request, 'pyment/add.html', context)

@login_required
def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            # Optionally add a success message using Django messages framework
            return redirect('employee_list_view')  # Redirect to employee detail view
    else:
        form = EmployeeForm(instance=employee)

   


    salaries = Salary.objects.filter(employee=employee).order_by('-effective_date')
   



    


    
    return render(request, 'employe/edit.html', {'form': form, 'employee': employee , 'salaries' : salaries})




def tc_input_view(request):
    if request.method == 'POST':
        form = TCForm(request.POST)
        if form.is_valid():
            tc = form.cleaned_data['tc']
            # Check if the TC exists in the Employee model
            employee = get_object_or_404(Employee, tc=tc)
            return redirect('serch_result', id=employee.id)
    else:
        form = TCForm()
    
    return render(request, 'employe/serch.html', {'form': form})





def searching_result(request, id):
   



    today = timezone.now().date()
    checking = False
    
    employee = get_object_or_404(Employee, id=id)
    attendance_records = Attendance.objects.filter(employee=employee).order_by('-date')
    attendance_today = Attendance.objects.filter(employee=employee, date=today).first()
    
    if attendance_today:
        message = "لقد تم تسجيل حضورك اليوم"
        checking = True
    else:
        message = "لم يتم تسجيل حضورك اليوم"
    
    # Get current year and month from request or default to current month
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)
    
    year = int(year)
    month = int(month)
    
    cal = Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Gather attendance for the entire month
    month_start = datetime(year, month, 1)
    month_end = month_start + timedelta(days=calendar.monthrange(year, month)[1])
    monthly_attendance = Attendance.objects.filter(employee=employee, date__range=[month_start, month_end])

    attendance_days = set(att.date.day for att in monthly_attendance)




    context = {
     
        'employee': employee,
        'attendance_records': attendance_records,
        'message': message,
        'checking': checking,
        'calendar': month_days,
        'attendance_days': attendance_days,
        'year': year,
        'month': month,
        'now': today,
        'month_name': month_start.strftime('%B'),
        'prev_year': (month_start - timedelta(days=1)).year,
        'prev_month': (month_start - timedelta(days=1)).month,
        'next_year': (month_end + timedelta(days=1)).year,
        'next_month': (month_end + timedelta(days=1)).month,
    }








    
    return render(request, 'employe/see.html', context)





def serch_result(request, id):
    pass




def serch_result_new(request, id):
    email = request.user.email if request.user.is_authenticated else None
    today = timezone.now().date()
    # get the current employe 
    employee = get_object_or_404(Employee, id=id)



 # get the  pyments  
    pyments = EmployeePayment.objects.filter(employee=employee)
    
    # Get current year and month from request or default to current month
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    
    # Gather attendance for the entire month
    month_start = datetime(year, month, 1)
    month_end = month_start + timedelta(days=calendar.monthrange(year, month)[1])
    monthly_attendance = Attendance.objects.filter(employee=employee, date__range=[month_start, month_end])
    
    # Create a set of days where attendance was recorded and their status
    attendance_days = set(att.date.day for att in monthly_attendance)
    attendance_status = {att.date.day: att.ispyed for att in monthly_attendance}
    
    # Check if attendance was recorded today
    attendance_today = Attendance.objects.filter(employee=employee, date=today).first()
    if attendance_today:
        message = "لقد تم تسجيل حضورك اليوم"
        cheking = True
    else:
        message = "لم يتم تسجيل حضورك اليوم"
        cheking = False
    
    # Get date range from request if available
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        attendance_records = Attendance.objects.filter(date__range=[from_date, to_date], employee=employee)
        payment_record = EmployeePayment.objects.filter(date__range=[from_date, to_date], employee=employee)

    else:
        attendance_records = Attendance.objects.filter(employee=employee)
        payment_record = EmployeePayment.objects.filter(employee=employee)


    
    attendance_count = attendance_records.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')
    pyment_cont = payment_record.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')

    unpaid_records = monthly_attendance.filter(ispyed=False)
    peyed_record = monthly_attendance.filter(ispyed=True).order_by('-date')[:5]
    count_all = attendance_records.count()
    count_pyed=payment_record.count()

    total_payments = payment_record.aggregate(total_amount=Sum('amount'))['total_amount'] or 0



    check_date = False

    if from_date is not None:
        check_date = True

    


    





    difference = count_all - count_pyed 

    diffrence_check = True
    if difference >0:

        messages = "لديك %s يوم غير مدفوع" % difference

        diffrence_check = True
    elif difference == 0:
         messages = "الحساب مغلق "
         diffrence_check = False
    else:
        messages = "يوم  %s لنا عليك  " % difference


    salary_details, total_salary = employee.calculate_salary_details()

   









    context = {
        'employee': employee,
        'from_date': from_date,
        'to_date': to_date,
        'attendance': monthly_attendance,
        'attendance_records': attendance_records,
        'attendance_count': attendance_count,
        "pyment_cont":pyment_cont,
        "difference" : difference,
        'message': message,
        "messages":messages,
        'check': cheking,
        "check_date" :check_date,

        'calendar': month_days,
        'attendance_days': attendance_days,
        'attendance_status': attendance_status,
        'year': year,
        'month': month,
        'now': today,
        'month_name': month_start.strftime('%B'),
        'prev_year': (month_start - timedelta(days=1)).year,
        'prev_month': (month_start - timedelta(days=1)).month,
        'next_year': (month_end + timedelta(days=1)).year,
        'next_month': (month_end + timedelta(days=1)).month,
        'unpaid_records': unpaid_records,
        'peyed_record' : peyed_record, 
        "email": email,
        "diffrence_check":diffrence_check,
        "pyments" : pyments,
        "total_payments" : total_payments,
        'salary_details': salary_details,
        'total_salary': total_salary,
    }
    
    return render(request, 'employe/serch_result_new.html', context)





def employee_report(request, id):
    employee = Employee.objects.get(id=id)

    # Get all payments for the employee
    payments = EmployeePayment.objects.filter(employee=employee)
    total_payments = payments.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Get attendance and calculate the total salary
    attendances = Attendance.objects.filter(employee=employee)
    salary_details, total_salary = employee.calculate_salary_details()

    context = {
        'employee': employee,
        'payments': payments,
        'total_payments': total_payments,
        'attendances': attendances,
        'salary_details': salary_details,
        'total_salary': total_salary,
    }

    return render(request, 'employe/report.html', context)





@login_required
def mark_as_paid(request, id):
    pass
 
@login_required

def delete_payment(request, id):
    if request.method == 'POST':
        payment = get_object_or_404(EmployeePayment, id=id)
        payment.remove()
     
     
        messages.success(request, 'Payment deleted successfully.')
    return redirect('employee_payment_view', id=payment.employee.id)




@login_required
def pyments(request):
    email = request.user.email if request.user.is_authenticated else None

    

        
        # Fetch the oldest x attendance records for the employee
    



    attendance_counts = (Attendance.objects.filter(ispyed=False).values('employee__id', 'employee__name', 'employee__position' ,"employee__age" ).annotate(attendance_days=Count('date')).order_by('-attendance_days')
    )
    context = {
        'attendance': attendance_counts,
        'email': email,

    }
        

        
    
    # If not a POST request, render a template or handle the GET request as needed
    return render(request, 'employe/pyment_list.html', context)



@login_required
def mark_attendance_paid(request, id):
    email = request.user.email if request.user.is_authenticated else None

  
    employee = get_object_or_404(Employee, pk=id)
    attendance = Attendance.objects.filter(employee=employee)

    unpaid_records = attendance.filter(ispyed=False)
    peyed_record = attendance.filter(ispyed=True).order_by('-date')[:10]
    if request.method == 'POST':
        form = MarkPaidForm(request.POST)
        if form.is_valid():
            number_of_records = form.cleaned_data['number_of_records']
            oldest_attendance_records = Attendance.objects.filter(employee=employee, ispyed=False).order_by('date')[:number_of_records]
            
            # Update the records in a separate step
            with transaction.atomic():
                for record in oldest_attendance_records:
                    record.ispyed = True
                    record.save()

            return redirect('serch_result', id=employee.id)  # Redirect to the employee detail page
    else:
        form = MarkPaidForm()

    context = {
        'form': form, 
        'employee': employee,
        "unpaid_records":unpaid_records,
        "peyed_record":peyed_record,
        "email":email,

        
        }

    
    return render(request, 'employe/pyment.html',  context)

def mark_all_attendance_paid(request, id):
    employee = get_object_or_404(Employee, pk=id)
    Attendance.objects.filter(employee=employee, ispyed=False).update(ispyed=True)
    return redirect('serch_result', id=employee.id)  # Redirect to the employee detail page




def serch_resul(request, id):
    pass



def employ_login_view(request):
    if request.method == 'POST':
        form = LogingForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('today_attaned_admin')  # Replace 'home' with the name of your home page URL
    else:
        form = LogingForm()
    
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)






def today_attaned(request):
     today = date.today()
     
     

        # Retrieve Attendance object or raise 404 if not found
     attendance = Attendance.objects.filter(date =today )



     context = {
        'attendance': attendance,
        'attendance_date': today,

    }



     return render(request, 'attendance/add_attend.html', context)

@login_required
def today_attaned_admin(request):
     email = request.user.email if request.user.is_authenticated else None
     today = date.today()
     
     

        # Retrieve Attendance object or raise 404 if not found
     attendance = Attendance.objects.filter(date =today )
     attendance_count = attendance.count()



     context = {
        'attendance': attendance,
        'attendance_date': today,
        'email' : email,
        'attendance_count' : attendance_count,

    }



     return render(request, 'attendance/add_attend_admin.html', context)


@login_required
def delete_attendance(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    
    attendance = get_object_or_404(Attendance, id=id)
    attendance.delete()
    return redirect('today_attaned_admin')




@login_required
def add_today(request):
     
    email = request.user.email if request.user.is_authenticated else None
    today = date.today()
    
    # Retrieve employees who have not attended today
    employees_not_attended_today = Employee.objects.filter(
        is_working=True
    ).exclude(
        attendance__date=today  # Assuming each attendance is linked to a user
    ).order_by('-state')
    
    context = {
        'employees_not_attended_today': employees_not_attended_today,
        'attendance_date': today,
        'email' : email
    }

    return render(request, 'attendance/adding.html', context)








@login_required
def add_attendance(request, id):
    email = request.user.email if request.user.is_authenticated else None
    employee = get_object_or_404(Employee, id=id)
    today = date.today()

    # Check if the attendance record already exists for today
    if Attendance.objects.filter(employee=employee, date=today).exists():
        messages.warning(request, f"Attendance for {employee.name} already exists for today.")
    else:
        # Create a new attendance record
        Attendance.objects.create(
            employee=employee,
            date=today,
            created_by=request.user,
            status='Present'  # or any other status you want to set
        )
        messages.success(request, f"Attendance for {employee.name} has been added.")

    return redirect('add_today')











# -- from to

@login_required
def attendance_views(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        attendance_records = Attendance.objects.filter(date__range=[from_date, to_date])
    else:
        attendance_records = Attendance.objects.all()

    attendance_count = attendance_records.values('employee__name').annotate(total_days=Count('date')).order_by('employee__name')

    context = {
        'from_date': from_date,
        'to_date': to_date,
        'attendance': attendance_records,
        'attendance_count': attendance_count
    }
    

    
    return render(request, 'attendance/from_to.html', context)




@login_required
def export_attendance_csv(request):
    # Create an HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_records.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['ID', 'Employee', 'Date', 'Created By', 'Status', 'Is Paid'])

    # Write data rows
    for record in Attendance.objects.all().values_list('id', 'employee', 'date', 'created_by', 'status', 'ispyed'):
        writer.writerow(record)

    return response



@login_required
# List View
def salary_list(request):
    employees = Employee.objects.filter(is_working=True)
    email = request.user.email if request.user.is_authenticated else None
    return render(request, 'salary/list.html', {'employees': employees , 'email':email})


@login_required
def salary_create(request, id):
    email = request.user.email if request.user.is_authenticated else None

    employee = Employee.objects.get(id=id)
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            salary = form.save(commit=False)
            salary.employee = employee
            salary.save()
            messages.success(request, 'Salary added successfully!')
            return redirect('edit_employee', id=employee.id)
    else:
        form = SalaryForm()

    last_salaries = Salary.objects.filter(employee=employee).order_by('-effective_date')
    context = {
        'employee': employee,
        'form': form,
        'last_salaries': last_salaries,
        'email': email
    }
    return render(request, 'salary/add.html', context)


@login_required

def salary_update_view(request, id , pk):

    employee = Employee.objects.get(id=id)
    email = request.user.email if request.user.is_authenticated else None
    # Fetch the Salary object to be updated
    salary = get_object_or_404(Salary, pk=pk)
    
    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            return redirect('edit_employee', id=employee.id)  # Redirect to the list view or another page after successful update
    else:
        form = SalaryForm(instance=salary)

    return render(request, 'salary/edit.html', {'form': form ,"email" :email , "employee" : employee})






def dashboard(request):
    # Get the total number of employees
    employes = Employee.objects.all()
    total_employees = Employee.objects.count()

    # Get the number of active and inactive employees
    active_employees = Employee.objects.filter(is_working=True).count()
    inactive_employees = Employee.objects.filter(is_working=False).count()

    # Get attendance data
    total_attendance = Attendance.objects.count()
    paid_attendances = Attendance.objects.filter(ispyed=True).count()
    unpaid_attendances = total_attendance - paid_attendances

    # Get total salaries and payments
    total_salaries = Salary.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_payments = EmployeePayment.objects.aggregate(total=Sum('amount'))['total'] or 0


    employees = [employee for employee in employes if employee.is_working and employee.calculate_balance() != 0]
    employees_total = [employee for employee in employes if employee.calculate_total_salaries != 0]
    total_balance = sum(employee.calculate_balance() for employee in employees)
    total_worked = sum(employee.calculate_total_salaries() for employee in employees_total)



    # Get recent payments
    recent_payments = EmployeePayment.objects.order_by('-date')[:10]

     #graph 
    attendance_data = Attendance.objects.filter(
        date__gte=timezone.now() - timedelta(days=30)
    ).values('date').annotate(count=Count('id')).order_by('date')

    dates = [entry['date'].strftime('%Y-%m-%d') for entry in attendance_data]
    counts = [entry['count'] for entry in attendance_data]

    # Create the graph
    fig = px.line(x=dates, y=counts, labels={'x': 'Date', 'y': 'Number of Attendances'}, title="Attendance Over Time")
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)





    payment_data = EmployeePayment.objects.filter(
        date__gte=timezone.now() - timedelta(days=30)
    ).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    # Prepare data for payment graph
    payment_dates = [entry['date'].strftime('%Y-%m-%d') for entry in payment_data]
    payment_totals = [entry['total_amount'] for entry in payment_data]

    # Create the payment graph
    payment_fig = px.line(x=payment_dates, y=payment_totals, labels={'x': 'Date', 'y': 'Total Payments'}, title="Payments Over Time")
    payment_graph_json = json.dumps(payment_fig, cls=plotly.utils.PlotlyJSONEncoder)















    # Prepare the context data to pass to the template
    context = {
          'payment_graph': mark_safe(payment_graph_json),
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'total_attendance': total_attendance,
        'paid_attendances': paid_attendances,
        'unpaid_attendances': unpaid_attendances,
        'total_salaries': total_salaries,
        'total_payments': total_payments,
        'recent_payments': recent_payments,
        'total_balance': total_balance,
        'total_worked': total_worked,
         'attendance_graph': mark_safe(graph_json),

    }

    return render(request, 'admin/dashboard.html', context)



from django.utils.safestring import mark_safe
import json
def checker(request):



    # Aggregate attendance data
    attendance_data = Attendance.objects.filter(
        date__gte=timezone.now() - timedelta(days=30)
    ).values('date').annotate(count=Count('id')).order_by('date')

    dates = [entry['date'].strftime('%Y-%m-%d') for entry in attendance_data]
    counts = [entry['count'] for entry in attendance_data]

    # Create the graph
    fig = px.line(x=dates, y=counts, labels={'x': 'Date', 'y': 'Number of Attendances'}, title="Attendance Over Time")
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

 

    payment_data = EmployeePayment.objects.filter(
        date__gte=timezone.now() - timedelta(days=30)
    ).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    # Prepare data for payment graph
    payment_dates = [entry['date'].strftime('%Y-%m-%d') for entry in payment_data]
    payment_totals = [entry['total_amount'] for entry in payment_data]

    # Create the payment graph
    payment_fig = px.line(x=payment_dates, y=payment_totals, labels={'x': 'Date', 'y': 'Total Payments'}, title="Payments Over Time")
    payment_graph_json = json.dumps(payment_fig, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        'attendance_graph': mark_safe(graph_json),
          'payment_graph': mark_safe(payment_graph_json),
    }








    return render(request, 'admin/dashboard.html', context)


  



@login_required
def Admin_add_employee(request):
    email = request.user.email if request.user.is_authenticated else None
    print(email)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            if not employee.created_by:  # Ensure not to override if already set
                employee.created_by = request.user.id  # Assuming you want to store the user ID
            employee.save()
            return redirect('employee_list_view')
    else:
        form = EmployeeForm()

    context = {
        'form': form,
        'email': email
    }
    return render(request, 'admin/employe/add.html', context)

