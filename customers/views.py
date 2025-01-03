# customers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import CustomUser
from .models import Costomers
from .forms import CostomersForm , CostomersFormAdvanv, ProfileImageForm , ChangePasswordForm
from biles.models import ProductHam , Package , Jar ,MainProduct  , ProductHam  , UdsBills  , UdsBill_inner , TrBills , TrBill_inner
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.utils.dateparse import parse_date

from django.http import HttpResponse
from django.template.loader import render_to_string

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from money.models import CustomerPaymentTl , CustomerPaymentUsd
from .forms import CustomerPaymentTlForm , CustomerPaymentUsdForm

from django.db.models import Q
from django.db.models import F 

from django.db.models import Sum

import json



from django.shortcuts import render
from django.http import JsonResponse
from .models import Costomers

def calculate_all_balances(request):
    # Fetch all customers
    customers = Costomers.objects.all()

    # Iterate through each customer and calculate balances
    for customer in customers:
        customer.calculate_balance_tl()
        customer.calculate_balance_usd()
    
    return JsonResponse({'status': 'success', 'message': 'Balances calculated for all customers.'})





def customer_bills_chart(request):
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        return redirect('customer_login')
    
    customer = get_object_or_404(Costomers, id=customer_id)
  
    bills = UdsBills.objects.filter(customer=customer).order_by('created_at')
    tr_biles = TrBills.objects.filter(customer=customer).order_by('created_at')

    # Prepare data for the chart
    dates = [bill.created_at.strftime('%Y-%m-%d') for bill in bills]
    prices = [bill.price for bill in bills]
    id = [bill.id for bill in bills]

    dates_tr = [tr_bile.created_at.strftime('%Y-%m-%d') for tr_bile in tr_biles]
    prices_tr = [tr_bile.price for tr_bile in tr_biles]
    id_tr = [tr_bile.id for tr_bile in tr_biles]





    total_price = bills.aggregate(Sum('price'))['price__sum'] or 0
    total_price_tr = tr_biles.aggregate(Sum('price'))['price__sum'] or 0

    formatted_price = '{:,}'.format(total_price)
    formatted_price_tr = '{:,}'.format(total_price_tr)


    context = {
        'dates': json.dumps(id),
        'prices': json.dumps(prices),
        'id':json.dumps(id),
        'total_price': formatted_price,


         'dates_tr': json.dumps(id_tr),
        'prices_tr': json.dumps(prices_tr),
        'id_tr':json.dumps(id_tr),
        'total_price_tr': formatted_price_tr,
         'customer': customer,



    }






    return render(request, 'customers/chart.html', context)





@login_required
def customer_bills_chart_admin(request,id):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
   
    
    customer = get_object_or_404(Costomers, id=id)

    if from_date and to_date:
        from_date = parse_date(from_date)
        to_date = parse_date(to_date)
  
        bills = UdsBills.objects.filter(created_at__range=[from_date, to_date], customer=customer).order_by('created_at')
        tr_biles = TrBills.objects.filter(created_at__range=[from_date, to_date],customer=customer).order_by('created_at')
    
    else:
         
        bills = UdsBills.objects.filter( customer=customer).order_by('created_at')
        tr_biles = TrBills.objects.filter(customer=customer).order_by('created_at')
    



    # Prepare data for the chart
    dates = [bill.created_at.strftime('%Y-%m-%d') for bill in bills]
    prices = [bill.price for bill in bills]
    id = [bill.id for bill in bills]

    dates_tr = [tr_bile.created_at.strftime('%Y-%m-%d') for tr_bile in tr_biles]
    prices_tr = [tr_bile.price for tr_bile in tr_biles]
    id_tr = [tr_bile.id for tr_bile in tr_biles]





    total_price = bills.aggregate(Sum('price'))['price__sum'] or 0
    total_price_tr = tr_biles.aggregate(Sum('price'))['price__sum'] or 0

    formatted_price = '{:,}'.format(total_price)
    formatted_price_tr = '{:,}'.format(total_price_tr)

  
    


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
         'customer': customer,



    }






    return render(request, 'admin/chart.html', context)




def update_cosomer(request):
    customer_id = request.session.get('customer_id')
    costomer = get_object_or_404(Costomers, pk=customer_id)
    
    if request.method == 'POST':
        form = CostomersForm(request.POST, instance=costomer)
        if form.is_valid():
            form.save()
            return redirect('customer_panel')  # Redirect to client detail page
    else:
        form = CostomersForm(instance=costomer)

    if not customer_id:
        return redirect('customer_login')
    return render(request, 'customers/edit.html', {'form': form , 'customer': costomer})



def edit_profile(request):


    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        return redirect('customer_login')
    

    customer = get_object_or_404(Costomers, id=customer_id)

   
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_panel')  # Replace with your success URL
    else:
        form = ProfileImageForm(instance=customer)
    return render(request, 'customers/img_edit.html', {'form': form , 'customer':customer })





def change_password(request):
    # Get the customer ID from the session
    customer_id = request.session.get('customer_id')

    if not customer_id:
        return redirect('customer_login')  # Redirect if no customer_id is found

    # Fetch the customer object or return 404 if not found
    customer = get_object_or_404(Costomers, id=customer_id)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_token = form.cleaned_data['token']
            # Update the customer's token
            customer.token = new_token
            customer.save()
            messages.success(request, 'Token changed successfully!')
            return redirect('customer_logout')  # Redirect to the success URL
    else:
        # Create a form instance with empty fields for initial display
        form = ChangePasswordForm()

    return render(request, 'customers/password.html', {'form': form, 'customer': customer})







def costomers_List(request):
    Costomers_List = Costomers.objects.filter(created_by=request.user.id)
    return render(request, 'admin/list.html', {'form': Costomers_List})


def fatch_costomers(request , id):

    costomer = Costomers.objects.get(pk=id)
   
    return render(request, 'customers/c_view.html', {'form': costomer})







def delete_costomers(request, id):
    costomer = Costomers.objects.filter(created_by=request.user.id)
    costomer_list = get_object_or_404(costomer, pk=id)
    if request.method == 'POST':
        costomer_list.delete()
        messages.success(request, 'ProductHamm deleted successfully.')
        return redirect('costomers_List')
    return render(request, 'ProductHam/view.html', {'form': costomer_list })






def customer_login(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        token = request.POST['token']
        try:
            customer = Costomers.objects.get(id=customer_id, token=token)
            # You may need to handle authentication logic here
            # For simplicity, we just set a session variable
            request.session['customer_id'] = customer.id
            return redirect('customer_panel')
        except Costomers.DoesNotExist:
            messages.error(request, 'Invalid customer ID or token')
            return redirect('customer_login')
    return render(request, 'customers/login.html')

def customer_login_tex(request):
    if request.method == 'POST':
        tex_no = request.POST.get('tex')  # Using .get() to avoid KeyError
        token = request.POST.get('token')  # Using .get() to avoid KeyError

        if tex_no and token:
            try:
                customer = Costomers.objects.get(tex=tex_no, token=token)
                request.session['customer_id'] = customer.id
                return redirect('customer_panel')
            except Costomers.DoesNotExist:
                messages.error(request, 'Invalid TEX number or token')
                return redirect('customer_login_tex')
        else:
            messages.error(request, 'TEX number and token are required')
            return redirect('customer_login_tex')

    return render(request, 'customers/login_tex.html')




@login_required
def add_costomer(request):
    if request.method == 'POST':
        form = CostomersFormAdvanv(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return redirect('customer_success')  # Redirect to a success page
    else:
        form = CostomersFormAdvanv()

    return render(request, 'customers/add.html', {'form': form})




def customer_panel(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer_login')
    customer = get_object_or_404(Costomers, id=customer_id)
    return render(request, 'navbar_costomer.html', {'customer': customer})



def customer_logout(request):
    try:
        del request.session['customer_id']
    except KeyError:
        pass
    return redirect('customer_login')







def fetch_bills_usd_list(request):


    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer_login')
    customer = get_object_or_404(Costomers, id=customer_id)


    bills = UdsBills.objects.filter(customer_id=customer_id).order_by('-created_at')
    
    return render(request, 'customers/bills_usd.html', {'form': bills ,'customer': customer} )



def view_bill(request ,id):

   

    customer_id = request.session.get('customer_id')
    costomer = Costomers.objects.filter(pk=customer_id)


    if not customer_id:
        bills = "no biles"
        # Handle the case where customer_id is not in the session
        

    # Fetch all UdsBills objects for the given customer

    bills = UdsBills.objects.filter(pk=id ,customer_id=customer_id )
    bill_instance = get_object_or_404(UdsBills,pk=id ,customer_id=customer_id)
    user_id = bill_instance.created_by.id
    records = UdsBill_inner.objects.filter(uds_bill= id)



    user = CustomUser.objects.filter(pk =user_id)




      
    return render(request, 'customers/usd_view.html', {'form': bills , 'form_in' :records  , 'costomer':costomer , 'user' : user })







def fetch_bills_tr_list(request):


    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer_login')
    customer = get_object_or_404(Costomers, id=customer_id)


    bills = TrBills.objects.filter(customer_id=customer_id).order_by('-created_at')
    
    return render(request, 'customers/bills_tr.html', {'form': bills ,'customer': customer} )





def view_bill_tr(request ,id):

   

    customer_id = request.session.get('customer_id')
    costomer = Costomers.objects.filter(pk=customer_id)


    if not customer_id:
        bills = "no biles"
        # Handle the case where customer_id is not in the session
        

    # Fetch all UdsBills objects for the given customer

    bills = TrBills.objects.filter(pk=id ,customer_id=customer_id )
    bill_instance = get_object_or_404(TrBills,pk=id ,customer_id=customer_id)
    user_id = bill_instance.created_by.id
    records = TrBill_inner.objects.filter(Tr_bill= id)



    user = CustomUser.objects.filter(pk =user_id)




      
    return render(request, 'customers/tr_view.html', {'form': bills , 'form_in' :records  , 'costomer':costomer , 'user' : user  , 'id':id})








def testt(request):
    return render(request, 'customers/index.html')



import uuid

@login_required
def edit_customer(request, id):
    customer = get_object_or_404(Costomers, id=id)

    if request.method == 'POST':
        form = CostomersFormAdvanv(request.POST, request.FILES, instance=customer)
        if not form.instance.token:  # If token is missing, generate it
            form.instance.token = uuid.uuid4().hex
        
        if form.is_valid():
            form.save()
            return redirect('customer_success')  # Redirect on success
        else:
            print(form.errors)  # Debugging form errors
            return render(request, 'admin/edting.html', {'form': form, 'customer': customer})
    else:
        form = CostomersFormAdvanv(instance=customer)
        if not form.instance.token:  # Ensure token is set for GET requests as well
            form.instance.token = uuid.uuid4().hex
    
    return render(request, 'admin/edting.html', {'form': form, 'customer': customer})


#admin add pyment tl  done

@login_required
def customer_paymenttl_view(request, customer_id):
    # Retrieve the customer for whom the payment is being made
    customer = get_object_or_404(Costomers, id=customer_id)
    form = CustomerPaymentTlForm()

    if request.method == 'POST':
        form = CustomerPaymentTlForm(request.POST)
        if form.is_valid():
            # Create a new payment without saving to database yet
            payment = form.save(commit=False)
            payment.customer = customer  # Set the customer for this payment
            payment.save()  # Save the payment

           
            customer.calculate_balance_tl()

           
            return redirect('customer_bills_chart_admin', id=customer.id)
    past_payments = CustomerPaymentTl.objects.filter(customer=customer).order_by('-date')

    return render(request, 'admin/paymentTl.html', {
        'form': form,
        'customer': customer,
        'past_payments': past_payments,
        'balance_tl': customer.balanceTr  # Display current balance
    })

#admin add pyment USD done

@login_required
def customer_paymentUSD_view(request, customer_id):
    
    customer = get_object_or_404(Costomers, id=customer_id)
    form = CustomerPaymentUsdForm()

    if request.method == 'POST':
        form = CustomerPaymentUsdForm(request.POST)
        if form.is_valid():
            # Create a new payment without saving to database yet
            payment = form.save(commit=False)
            payment.customer = customer  # Set the customer for this payment
            payment.save()  # Save the payment

            return redirect('customer_bills_chart_admin', id=customer.id)

    # Retrieve all past payments for the customer
    past_payments = CustomerPaymentUsd.objects.filter(customer=customer).order_by('-date')

    return render(request, 'admin/paymentUsd.html', {
        'form': form,
        'customer': customer,
        'past_payments': past_payments,
        'balance_tl': customer.balanceUsd  # Display current balance
    })



@login_required
def delete_paymentokusd(request, id):
    payment = get_object_or_404(CustomerPaymentUsd, id=id)
        
    payment.delete()
    messages.success(request, 'Payment deleted successfully.')
    return redirect('add_payment_and_list_usd', customer_id=payment.customer.id)

    # Render confirmation page if it's a GET request
   



@login_required
def delete_paymentTr(request, id):
    payment = get_object_or_404(CustomerPaymentTl, id=id)


    # Render confirmation page if it's a GET request
    return render(request, 'admin/deletePymentTr.html', {'payment': payment})



@login_required
def delete_paymentokTr(request, id):
    payment = get_object_or_404(CustomerPaymentTl, id=id)
        
    payment.delete()
    messages.success(request, 'Payment deleted successfully.')
    return redirect('add_payment_and_list_tr', customer_id=payment.customer.id)

    # Render confirmation page if it's a GET request
   




@login_required
def customer_list_view(request):
    query = request.GET.get('q', '')  # Get the search query from the GET parameters, default to an empty string
    if query:
        # Split the query into separate words and filter based on each word
        words = query.split()
        filters = Q()
        for word in words:
            filters |= Q(name__icontains=word) | Q(pk__icontains=word) | Q(tex__icontains=word) 

            
        
        customers = Costomers.objects.filter(filters)
    else:
        customers = Costomers.objects.all()
    
    return render(request, 'admin/chat/tr.html', {'customers': customers, 'query': query})




@login_required
def billsTL_and_payments_view(request, customer_id):
    customer = get_object_or_404(Costomers, id=customer_id)
    bills = TrBills.objects.filter(customer=customer).values('id', 'created_at', 'price', 'note', 'is_paid')
    payments = CustomerPaymentTl.objects.filter(customer=customer).values('id', 'date', 'amount', 'note')

    combined = []
    for bill in bills:
        print(bill)
        combined.append({
            'id': bill['id'],
            'date': bill['created_at'],
            'message': f"فاتورة بتاريخ {bill['created_at']} بقيمة {'{:,}'.format(bill['price'])} ليرة تركية. الملاحظة: {bill['note']}",
            'type': 'bill',
        })
    for payment in payments:
        combined.append({
            'id': payment['id'],
            'date': payment['date'],
            'message': f"دفعة بقيمة {'{:,}'.format(payment['amount'])} بتاريخ {payment['date']}. الملاحظة: {payment['note']}",
            'type': 'payment',
        })

    combined.sort(key=lambda x: x['date'])


    balance = '{:,}'.format(customer.balanceTr)

    return JsonResponse({
        'customer': {
            'name': customer.name,
            'profile_image': customer.profile_image.url if customer.profile_image else 'https://cdn-icons-png.flaticon.com/512/3686/3686930.png',
            'balance' : balance
        },
        'items': combined
    })















@login_required
def costomer_chat_usd(request):

    query = request.GET.get('q', '')  # Get the search query from the GET parameters, default to an empty string
    if query:
        # Split the query into separate words and filter based on each word
        words = query.split()
        filters = Q()
        for word in words:
            filters |= Q(name__icontains=word) | Q(pk__icontains=word) | Q(tex__icontains=word) 

            
        
        customers = Costomers.objects.filter(filters)
    else:
        customers = Costomers.objects.all()


    return render(request, 'admin/chat/usd.html', {'customers': customers , 'query':query })





@login_required
def billsusd_and_payments_view(request, customer_id):
    customer = get_object_or_404(Costomers, id=customer_id)
    customer.calculate_balance_usd()
    customer.save()
    bills = UdsBills.objects.filter(customer=customer).values('id', 'created_at', 'price', 'note', 'is_paid')
    payments = CustomerPaymentUsd.objects.filter(customer=customer).values('id', 'date', 'amount', 'note')

    combined = []
    for bill in bills:
       
        combined.append({
            'id': bill['id'],
            'date': bill['created_at'],
            'message': f"فاتورة بتاريخ {bill['created_at']} بقيمة {'{:,}'.format(bill['price'])} ]دلر  . الملاحظة: {bill['note']}",
            'type': 'bill',
        })



    for payment in payments:
        combined.append({
            'id': payment['id'],
            'date': payment['date'],
            'message': f"دفعة بقيمة {'{:,}'.format(payment['amount'])} بتاريخ {payment['date']}. الملاحظة: {payment['note']}",
            'type': 'payment',
        })

    combined.sort(key=lambda x: x['date'])

    balance = '{:,}'.format(customer.balanceUsd)

    return JsonResponse({
        'customer': {
            'name': customer.name,
            'profile_image': customer.profile_image.url if customer.profile_image else 'https://cdn-icons-png.flaticon.com/512/3686/3686930.png',
                'balance' : balance
        },
        'items': combined
    })










def add_payment_and_list_usd(request, customer_id):
    from django.utils.dateparse import parse_date
    from django.core.paginator import Paginator

    # Get the client based on the ID passed in the URL
    customer = get_object_or_404(Costomers, id=customer_id)

    # Get the start_date and end_date from query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Parse dates and handle None values
    start_date = parse_date(start_date) if start_date not in [None, "None", ""] else None
    end_date = parse_date(end_date) if end_date not in [None, "None", ""] else None

    # Filter payments based on date range if provided
    payments = CustomerPaymentUsd.objects.filter(customer=customer).order_by('-date')
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
        form = CustomerPaymentUsdForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = customer
            payment.save()
            messages.success(request, f"Payment of {payment.amount} USD t added successfully for customer   {customer.name}.  pk :{payment.pk} ")
            return redirect('customer_bills_chart_admin', id=customer.id)
    else:
        form = CustomerPaymentUsdForm()

    return render(request, 'admin/payment_Usd.html', {
        'form': form,
        'payments': payments,
        'customer': customer,
        'show_all': show_all,
        'start_date': start_date,
        'end_date': end_date,
    })









def add_payment_and_list_tr(request, customer_id):
    from django.utils.dateparse import parse_date
    from django.core.paginator import Paginator

    # Get the client based on the ID passed in the URL
    customer = get_object_or_404(Costomers, id=customer_id)

    # Get the start_date and end_date from query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Parse dates and handle None values
    start_date = parse_date(start_date) if start_date not in [None, "None", ""] else None
    end_date = parse_date(end_date) if end_date not in [None, "None", ""] else None

    # Filter payments based on date range if provided
    payments = CustomerPaymentTl.objects.filter(customer=customer).order_by('-date')
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
        form = CustomerPaymentTlForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = customer
            payment.save()
            messages.success(request, f"Payment of {payment.amount} tl  added successfully for customer   {customer.name}.  pk :{payment.pk} ")
            return redirect('customer_bills_chart_admin', id=customer.id)
    else:
        form = CustomerPaymentTlForm()

    return render(request, 'admin/payment_tr.html', {
        'form': form,
        'payments': payments,
        'customer': customer,
        'show_all': show_all,
        'start_date': start_date,
        'end_date': end_date,
    })



