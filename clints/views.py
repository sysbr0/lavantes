# customers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import CustomUser
from .models import *
from .forms import *

from django.db.models import Value, CharField

from biles.models import ProductHam , Package , Jar ,MainProduct  , ProductHam  , UdsBills  , UdsBill_inner , TrBills , TrBill_inner
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.utils.dateparse import parse_date

from django.http import HttpResponse
from django.template.loader import render_to_string

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from money.models import CustomerPaymentTl , CustomerPaymentUsd


from django.db.models import Q
from django.db.models import F 

from django.db.models import Sum

import json

from django.shortcuts import render
from main.models import *

# Create your views here.
def fatch_clints(self):
    pass




@login_required
def clint_bills_chart_admin(request,id):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
   
    
    clint = get_object_or_404(clints, pk=id)

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
  
     
        tr_biles = GeneralBuying.objects.filter(created_at__range=[from_date, to_date],client=clint).order_by('created_at')
        pyments = ClintPayment.objects.filter(date__range=[from_date , to_date],clint=clint).order_by('date')

    
    else:
         
        tr_biles = GeneralBuying.objects.filter(client=clint).order_by('created_at')
        pyments = ClintPayment.objects.filter(clint=clint).order_by('date')
    







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
        "clint":clint,

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




    return render(request, 'admin/charts.html', context)



















@login_required
def clint_chat(request):
    customers = clints.objects.all()
    return render(request, 'admin/chat/index.html', {'customers': customers})

@login_required
def bills_and_payments_view(request, id):
    clint = get_object_or_404(clints, id=id)
    clint.save()
  
    bills = GeneralBuying.objects.filter(client=clint).values('id', 'buying_type', 'created_at', 'price', 'notee')
    payments = ClintPayment.objects.filter(clint=clint).values('id', 'date', 'amount', 'note' , 'image')

    combined = []
    for bill in bills:
       
        combined.append({
            'id': bill['id'],
            'date': bill['created_at'],
            'message': f"فاتورة بتاريخ {bill['created_at']} بقيمة {'{:,}'.format(bill['price'])}   . الملاحظة: {bill['notee']} . نوع العملية: {bill['buying_type']}  " ,
            'type': 'bill',
        })



    for payment in payments:
        combined.append({
            'id': payment['id'],
            'date': payment['date'],
            'message': f"دفعة بقيمة {'{:,}'.format(payment['amount'])} بتاريخ {payment['date']}. الملاحظة: {payment['note']}   ",
            'type': 'payment',
        })

    combined.sort(key=lambda x: x['date'])
    print(clint.get_total_payment())

    balance = '{:,}'.format(clint.calculate())

    return JsonResponse({
        'customer': {
            'name': clint.name,
            'profile_image': clint.profile_image.url if clint.profile_image else 'https://cdn-icons-png.flaticon.com/512/3686/3686930.png',
            'balance' : balance
        },
        'items': combined
    })








from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ClintPayment, clints
from .forms import ClintPymantForm




from django.db.models import Q
from django.utils.dateparse import parse_date



def add_payment_and_list(request, clint_id):
    from django.utils.dateparse import parse_date
    from django.core.paginator import Paginator

    # Get the client based on the ID passed in the URL
    clint = get_object_or_404(clints, id=clint_id)

    # Get the start_date and end_date from query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Parse dates and handle None values
    start_date = parse_date(start_date) if start_date not in [None, "None", ""] else None
    end_date = parse_date(end_date) if end_date not in [None, "None", ""] else None

    # Filter payments based on date range if provided
    payments = ClintPayment.objects.filter(clint=clint).order_by('-date')
    if start_date:
        payments = payments.filter(date__gte=start_date)
    if end_date:
        payments = payments.filter(date__lte=end_date)

    # Handle "show_all" parameter
    show_all = request.GET.get('show_all', False)
    if not show_all:
        paginator = Paginator(payments, 10)  # Show 10 payments per page
        page_number = request.GET.get('page')
        payments = paginator.get_page(page_number)

    # Handle form submission
    if request.method == 'POST':
        form = ClintPymantForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.clint = clint
            payment.save()
            messages.success(request, f"Payment of {payment.amount} added successfully for {clint.name}.")
            return redirect('add-payment', clint_id=clint.id)
    else:
        form = ClintPymantForm()

    return render(request, 'admin/payment_form.html', {
        'form': form,
        'payments': payments,
        'clint': clint,
        'show_all': show_all,
        'start_date': start_date,
        'end_date': end_date,
    })





@login_required
def edit_clintPymant(request, pk):
    # Retrieve the existing GeneralBuying record
    pymant = get_object_or_404(ClintPayment, pk=pk)

    if request.method == 'POST':
        form = ClintPymantForm(request.POST, instance=pymant)  # Pre-fill the form
        if form.is_valid():
            
            form.save()
            return redirect('general_buying_list')  # Redirect to the list after saving
    else:
        form = ClintPymantForm(instance=pymant)  # Pre-fill the form for GET request





    return render(request, 'pyment/edit.html', {'form': form, 'pyment': pymant})




def delete_payment(request, payment_id):
    payment = get_object_or_404(ClintPayment, id=payment_id)
    clint_id = payment.clint.id  # Save the client ID for redirecting later
    payment.delete()  # Delete the payment record
    messages.success(request, "Payment deleted successfully.")  # Add success message
    return redirect('add-payment', clint_id=clint_id)








def customer_bills_chart(request):
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        return redirect('customer_login')
    
    customer = get_object_or_404(clints, id=customer_id)
  

    tr_biles = GeneralBuying.objects.filter(client=customer).order_by('created_at')

    # Prepare data for the chart
   

    dates_tr = [tr_bile.created_at.strftime('%Y-%m-%d') for tr_bile in tr_biles]
    prices_tr = [tr_bile.price for tr_bile in tr_biles]
    id_tr = [tr_bile.id for tr_bile in tr_biles]





    total_price_tr = tr_biles.aggregate(Sum('price'))['price__sum'] or 0


    formatted_price_tr = '{:,}'.format(total_price_tr)


    context = {
        'dates': json.dumps(id),
  
        'id':json.dumps(id),

         'dates_tr': json.dumps(id_tr),
        'prices_tr': json.dumps(prices_tr),
        'id_tr':json.dumps(id_tr),
        'total_price_tr': formatted_price_tr,
         'customer': customer,
    }









@login_required
def clint_bills_chart_admin1(request,id):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
   
    
    clint = get_object_or_404(clints, id=id)

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
  
      
        tr_biles = GeneralBuying.objects.filter(created_at__range=[from_date, to_date],client=clint).order_by('created_at')
    
    else:
         
 
        tr_biles = GeneralBuying.objects.filter(client=clint).order_by('created_at')
    



    dates_tr = [tr_bile.created_at.strftime('%Y-%m-%d') for tr_bile in tr_biles]
    prices_tr = [tr_bile.price for tr_bile in tr_biles]
    id_tr = [tr_bile.pk for tr_bile in tr_biles]





  
    total_price_tr = tr_biles.aggregate(Sum('price'))['price__sum'] or 0


    formatted_price_tr = '{:,}'.format(total_price_tr)

  
    


    context = {
  
        'form_tr':tr_biles,
        'dates': json.dumps(id),
  
        'id':json.dumps(id),


         'dates_tr': json.dumps(id_tr),
        'prices_tr': json.dumps(prices_tr),
        'id_tr':json.dumps(id_tr),
        'total_price_tr': formatted_price_tr,
         'clints': clint,



    }











@login_required
def bills_chart_admin(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
   
    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
        # Filter the queryset based on date range
        tr_biles = GeneralBuying.objects.filter(created_at__range=[from_date, to_date]).order_by('created_at')
        pyments = ClintPayment.objects.filter(date__range=[from_date , to_date]).order_by('date')
    else:
        # If no date range, get all the GeneralBuying records
        tr_biles = GeneralBuying.objects.all().order_by('created_at')
        pyments = ClintPayment.objects.all().order_by('date')

    # Get the total price of all the records before pagination
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

    balance = total_price_tr - total_pymant

    context = {
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
        'balance': balance,
    }

    return render(request, 'admin/clintchart2.html', context)






@login_required
def client_report(request, client_id):
    # Fetch client information
    client = get_object_or_404(clints, id=client_id)
    
    # Fetch GeneralBuying transactions for the client
    general_buyings = GeneralBuying.objects.filter(client=client).annotate(
        transaction_type=Value('General Buying', output_field=CharField()),
        date=F('created_at')  # Alias `created_at` to `date` for consistency
    ).values('date', 'price', 'notee', 'transaction_type')
    total_general_buying = GeneralBuying.objects.filter(client=client).aggregate(
        total_spent=Sum('price')
    )['total_spent'] or 0


    total_clint_payments = ClintPayment.objects.filter(clint=client).aggregate(
        total_spent=Sum('amount')
    )['total_spent'] or 0


    
    # Fetch ClintPayment transactions for the client
    clint_payments = ClintPayment.objects.filter(clint=client).annotate(
        transaction_type=Value('Client Payment', output_field=CharField()),
        price=F('amount'),  # Alias `amount` to `price` for consistency
        notee=F('note'),    # Alias `note` to `notee` for consistency
        is_payment=Value(True, output_field=CharField())  # Add flag for payment
    ).values('date', 'price', 'notee', 'transaction_type', 'is_payment')

    # Add `is_payment` field to GeneralBuying for consistency
    general_buyings = general_buyings.annotate(is_payment=Value(False, output_field=CharField()))
    
    # Combine and sort transactions by date in descending order
    transactions = sorted(
        list(general_buyings) + list(clint_payments),
        key=lambda x: x['date'],
        reverse=True
    )



    if  total_general_buying > total_clint_payments :
        balance= True
    else:
        balance = False
    



    
    # Render data to the template
    context = {
        'client': client,
        'profile_image': client.profile_image.url if client.profile_image else 'https://cdn-icons-png.flaticon.com/512/3686/3686930.png',
        'transactions': transactions,
        'buy': total_general_buying,
        'pay': total_clint_payments,
        'balance': balance,

    }
    return render(request, 'admin/report.html', context)
