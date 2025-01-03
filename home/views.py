from django.shortcuts import render , get_object_or_404 , redirect

import json
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from biles.models import *
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from customers.models import *
from employe.models import *
from django.db.models import Count
from main.models import *
from clints.models import *


def home(request):
    # Perform some logic here
    return redirect('https://web.alsayidnavi.com/')






@login_required
def chart(request):

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')


    employes = Employee.objects.all()

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
  
        #start of biles chart
        bills_char = UdsBills.objects.filter(created_at__range=[from_date, to_date]).values('id', 'price','created_at')
        tr_biles_char = TrBills.objects.filter(created_at__range=[from_date, to_date]).values('id', 'price' , 'created_at')
        #end of billes chart

         #start of employe chart

        attendances = Attendance.objects.filter(date__range=[from_date, to_date]).order_by('date')
        payments = EmployeePayment.objects.filter(date__range=[from_date , to_date]).order_by('date')
         #end of employe chart
         #start of  clint chart


        tr_biles = GeneralBuying.objects.filter(created_at__range=[from_date, to_date]).order_by('created_at')
        pyments = ClintPayment.objects.filter(date__range=[from_date , to_date]).order_by('date')
        #end of  clint chart
    
    else:
     
        bills_char = UdsBills.objects.all().values('id', 'price', 'created_at')
        tr_biles_char = TrBills.objects.all().values('id', 'price' , 'created_at')

         #end of billes chart

         #start of employe chart

        attendances = Attendance.objects.all().order_by('date')
        payments = EmployeePayment.objects.all().order_by('date')

          #end of employe chart
         #start of  clint chart

        tr_biles = GeneralBuying.objects.all().order_by('created_at')
        pyments = ClintPayment.objects.all().order_by('date')
        #end of  clint chart





    usdids = [bill['id'] for bill in bills_char]
    usdprices = [bill['price'] for bill in bills_char]

    trids = [bill['id'] for bill in tr_biles_char]
    trprices = [bill['price'] for bill in tr_biles_char]

    balance_summary = Costomers.objects.aggregate(
        total_balance_usd=Sum('balanceUsd'),
        total_balance_tr=Sum('balanceTr')
    )

    bills_monthly = (
        bills_char.annotate(month=TruncMonth('created_at'))
             .values('month')
             .annotate(total_price=Sum('price'))
             .order_by('month')
    )

    tr_bills_monthly = (
        tr_biles_char.annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(total_price=Sum('price'))
                .order_by('month')
    )


    total_price = bills_char.aggregate(Sum('price'))['price__sum'] or 0
    total_price_tr = tr_biles_char.aggregate(Sum('price'))['price__sum'] or 0
    formatted_price = '{:,}'.format(total_price)
    formatted_price_tr = '{:,}'.format(total_price_tr)
    months = [entry['month'].strftime('%Y-%m') for entry in bills_monthly]
    months_tr = [entry['month'].strftime('%Y-%m') for entry in tr_bills_monthly]
   
    bills_monthly = (
        bills_char.annotate(month=TruncMonth('created_at'))
             .values('month')
             .annotate(total_price=Sum('price'))
             .order_by('month')
    )
    # Calculate monthly totals for TrBills
    tr_bills_monthly = (
        tr_biles_char.annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(total_price=Sum('price'))
                .order_by('month')
    )

    # Format data for charts
    months_usd = [entry['month'].strftime('%Y-%m') for entry in bills_monthly]
    totals_usd = [entry['total_price'] for entry in bills_monthly]

    months_tr = [entry['month'].strftime('%Y-%m') for entry in tr_bills_monthly]
    totals_tr = [entry['total_price'] for entry in tr_bills_monthly]

    # Combine data for the chart
    chart_data = {
        'months': months_usd + [m for m in months_tr if m not in months_usd],
        'usd_totals': totals_usd,
        'tr_totals': totals_tr,
    }


#start of the employe chart 


    total_attendance_count = attendances.count()

    total_payment = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    formatted_payment = '{:,}'.format(total_payment)

   # employees = [employee for employee in employes if employee.is_working and employee.calculate_balance() != 0]

    total_balance = 0 #sum(employee.calculate_balance() for employee in employees)


    dates_attendance = [attendance.date.strftime('%Y-%m-%d') for attendance in attendances]
    attendance_counts = [1 for _ in attendances]  # Each attendance record counts as 1 (you can modify this logic)
    id_attendance = [attendance.pk for attendance in attendances]

    dates_payment = [payment.date.strftime('%Y-%m-%d') for payment in payments]
    payment_amounts = [float(payment.amount) for payment in payments]  # Convert Decimal to float
    id_payment = [payment.pk for payment in payments]

    balance = total_payment  # Assuming you're keeping balance as total payment in this case

   
    attendance_counts_by_date = (
        attendances
        .values('date')  # Group by the 'date' field
        .annotate(count=Count('pk'))  # Count the number of attendance records for each date
        .order_by('date')  # Order the result by date
    )

  

    # Prepare data for the chart
    dates = [attendance['date'].strftime('%Y-%m-%d') for attendance in attendance_counts_by_date]
    attendance_counts = [attendance['count'] for attendance in attendance_counts_by_date]
















    total_price_tr = tr_biles.aggregate(Sum('price'))['price__sum'] or 0
    formatted_price_tr = '{:,}'.format(total_price_tr)

    total_pymant = pyments.aggregate(Sum('amount'))['amount__sum'] or 0
    formatted_price_pyment = '{:,}'.format(total_pymant)

    # Handle pagination
    show_all = request.GET.get('show_all', False)
    if not show_all:
        from django.core.paginator import Paginator
        paginator = Paginator(tr_biles, 10)  # Show 10 bills per page
        page_number = request.GET.get('page')
        tr_biles = paginator.get_page(page_number)

    # Prepare data for chart
    dates_tr = [tr_bile.created_at.strftime('%Y-%m-%d') for tr_bile in tr_biles]
    prices_tr = [float(tr_bile.price) for tr_bile in tr_biles]  # Convert Decimal to float
    id_tr = [tr_bile.pk for tr_bile in tr_biles]

    dates_pyment = [pymant.date.strftime('%Y-%m-%d') for pymant in pyments]
    prices_pyment = [float(pymant.amount) for pymant in pyments]  # Convert Decimal to float
    id_pyment = [pymant.pk for pymant in pyments]

    clint_balance = total_price_tr - total_pymant


    
    context = {
     
       
        'total_price': formatted_price,
        'total_price_tr': formatted_price_tr,
         'months': json.dumps(months),
        'months_tr': json.dumps(months_tr),
        'chart_data': json.dumps(chart_data),
        'total_price_usd': '{:,}'.format(bills_char.aggregate(Sum('price'))['price__sum'] or 0),
        'balance_summary':balance_summary,
        'usdids':usdids,
        'trids':trids,
        'usdprices':usdprices,
        'trprices':trprices,


        #end of tr billes or usd biles 

        'dates': json.dumps(dates),
        'attendance_counts': json.dumps(attendance_counts),
        'attendances': attendances,
        'attendance_counts_by_date': attendance_counts_by_date,
        'dates_attendance': json.dumps(dates_attendance),
        'dates_payment': json.dumps(dates_payment),
        'payment_amounts': json.dumps(payment_amounts),
        'id_attendance': json.dumps(id_attendance),
        'id_payment': json.dumps(id_payment),
        'total_attendance_count': total_attendance_count,
        'total_payment': formatted_payment,
        'balance': balance,
        'total_balance': total_balance,
       

         #end of employe chart 


        'form_tr': tr_biles,
        'dates_tr': json.dumps(dates_tr),
        'dates_pyment': json.dumps(dates_pyment),
        'prices_tr': json.dumps(prices_tr),
        'prices_pyment': json.dumps(prices_pyment),
        'id_tr': json.dumps(id_tr),
        'id_pyment': json.dumps(id_pyment),
        'total_price_tr': formatted_price_tr,
        'total_pymant': formatted_price_pyment,
        'show_all': show_all,
        'clint_balance': clint_balance,



    }
    return render(request, 'admin/chart_dashbord.html', context)






