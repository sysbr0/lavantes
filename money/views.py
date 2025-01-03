from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import MoneySource , GeneralPayment
from .forms import MoneySourceForm

from django.db.models.functions import TruncMonth

from django.utils.dateparse import parse_date


import json
from biles.models import ProductHam , Package , Jar ,MainProduct  , ProductHam  , UdsBills  , UdsBill_inner , TrBills , TrBill_inner
from django.db.models import Sum

from django.contrib.auth.decorators import login_required 


# List View
def money_source_list(request):
    moneysources = MoneySource.objects.all()
    return render(request, 'money/list.html', {'moneysources': moneysources})

# Create View
def money_source_create(request):
    if request.method == 'POST':
        form = MoneySourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('moneysource_list'))
    else:
        form = MoneySourceForm()
    return render(request, 'money/add.html', {'form': form})

# Update View
def money_source_update(request, pk):
    moneysource = get_object_or_404(MoneySource, pk=pk)
    if request.method == 'POST':
        form = MoneySourceForm(request.POST, instance=moneysource)
        if form.is_valid():
            form.save()
            return redirect(reverse('moneysource_list'))
    else:
        form = MoneySourceForm(instance=moneysource)
    return render(request, 'money/edit.html', {'form': form})

# Delete View
def money_source_delete(request, pk):
    moneysource = get_object_or_404(MoneySource, pk=pk)
    if request.method == 'POST':
        moneysource.delete()
        return redirect(reverse('moneysource_list'))
    return render(request, 'money/delete.html', {'object': moneysource})





def genaral_pyment_list(request):

    
    GeneralPayments = GeneralPayment.objects.all()


    return render(request, 'pyment/list2.html', {'GeneralPayment': GeneralPayments})

@login_required
def bills_chart_admin(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
   
    


    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
  
        bills = UdsBills.objects.filter(created_at__range=[from_date, to_date]).order_by('-created_at')
        tr_biles = TrBills.objects.filter(created_at__range=[from_date, to_date]).order_by('-created_at')
    
    else:
         
        bills = UdsBills.objects.all().order_by('-created_at')
        tr_biles = TrBills.objects.all().order_by('-created_at')
    



    # Prepare data for the chart
    dates = [bill.created_at.strftime('%Y-%m-%d') for bill in bills]
    prices = [bill.price for bill in bills]
    id = [bill.id for bill in bills]

    dates_tr = [tr_bile.created_at.strftime('%Y-%m-%d') for tr_bile in tr_biles]
    prices_tr = [tr_bile.price for tr_bile in tr_biles]
    id_tr = [tr_bile.id for tr_bile in tr_biles]



    bills_monthly = (
        bills.annotate(month=TruncMonth('created_at'))
             .values('month')
             .annotate(total_price=Sum('price'))
             .order_by('month')
    )

    tr_bills_monthly = (
        tr_biles.annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(total_price=Sum('price'))
                .order_by('month')
    )






    total_price = bills.aggregate(Sum('price'))['price__sum'] or 0
    total_price_tr = tr_biles.aggregate(Sum('price'))['price__sum'] or 0

    formatted_price = '{:,}'.format(total_price)
    formatted_price_tr = '{:,}'.format(total_price_tr)


    months = [entry['month'].strftime('%Y-%m') for entry in bills_monthly]
    prices = [entry['total_price'] for entry in bills_monthly]

    months_tr = [entry['month'].strftime('%Y-%m') for entry in tr_bills_monthly]
    prices_tr = [entry['total_price'] for entry in tr_bills_monthly]




    bills_monthly = (
        bills.annotate(month=TruncMonth('created_at'))
             .values('month')
             .annotate(total_price=Sum('price'))
             .order_by('month')
    )
    # Calculate monthly totals for TrBills
    tr_bills_monthly = (
        tr_biles.annotate(month=TruncMonth('created_at'))
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






  
    


    context = {
        'form':bills,
        'form_tr':tr_biles,
        'dates': json.dumps(id),
        'prices': json.dumps(prices),
        'id':json.dumps(id),
        'total_price': formatted_price,


         'dates_tr': json.dumps(id_tr),
        'prices_tr': json.dumps(prices_tr),
        'id_tr':json.dumps(id_tr),
        'total_price_tr': formatted_price_tr,

         'months': json.dumps(months),
       
        'months_tr': json.dumps(months_tr),
       




       'bills': bills,
        'tr_biles': tr_biles,
        'chart_data': json.dumps(chart_data),
        'total_price_usd': '{:,}'.format(bills.aggregate(Sum('price'))['price__sum'] or 0),
        




    }






    return render(request, 'chart.html', context)










