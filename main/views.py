


# Create your views here.
# views.py 
from django.shortcuts import render, redirect , get_object_or_404
from .forms import *

from django.contrib import messages
from django.http import HttpResponse
from django.utils.encoding import smart_str  # Import smart_str for encoding
from clints.models import *
from .models import *
from users.models import CustomUser

from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from clints.models import *
from django.utils.timezone import datetime
from clints.forms import *


from django.urls import reverse_lazy


import csv
from django.shortcuts import redirect



def swiching(request , pk , name):
    url ="buying_"+name

    return redirect(url, pk=pk)



def home(request):
    # Perform some logic here
    return redirect('https://web.alsayidnavi.com/')


def test(self):
    pass

from .models import GeneralBuying
from .forms import GeneralBuyingForm
from django.utils.dateparse import parse_date




@login_required
def general_buying_list(request):



    if request.method == 'POST':
        form = GeneralBuyingForm(request.POST)
        if form.is_valid():
            general = form.save(commit=False)
            # Save the form and get the saved instance
            general.created_by = request.user  # Assign the current user
            general.save()

            # Redirect to the 'swiching' view using reverse with parameters
            return redirect('general_buying_list')
    else:
        form = GeneralBuyingForm()


       
    start_date_str = request.POST.get('start_date', '')
    end_date_str = request.POST.get('end_date', '')
    start_date = parse_date(start_date_str) if start_date_str else None
    end_date = parse_date(end_date_str) if end_date_str else None
    
    if start_date and end_date:
        general_buyings = GeneralBuying.objects.filter(created_at__range=(start_date, end_date))
    else:
    
         general_buyings = GeneralBuying.objects.all()
    return render(request, 'general/buying_list.html', {'general_buyings': general_buyings, 'form':form} )









@login_required
def create_general_buying(request):
    if request.method == 'POST':
        form = GeneralBuyingForm(request.POST)
        if form.is_valid():
            general = form.save(commit=False)
            # Save the form and get the saved instance
            general.created_by = request.user  # Assign the current user
            general.save()

            # Redirect to the 'swiching' view using reverse with parameters
            return redirect('general_buying_list')
    else:
        form = GeneralBuyingForm()

    return render(request, 'general/buying_form.html', {'form': form})


@login_required
def edit_general_buying(request, pk):
    # Retrieve the existing GeneralBuying record
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    if request.method == 'POST':
        form = GeneralBuyingForm(request.POST, instance=general_buying)  # Pre-fill the form
        if form.is_valid():
            
            form.save()
            return redirect('general_buying_list')  # Redirect to the list after saving
    else:
        form = GeneralBuyingForm(instance=general_buying)  # Pre-fill the form for GET request

    return render(request, 'general/buying_form_edit.html', {'form': form, 'general_buying': general_buying})



def delete_general_buying(request, pk):

    general_buying = get_object_or_404(GeneralBuying, pk=pk)
    general_buying.delete()
    return redirect('general_buying_list') 
  


@login_required
def view(request ,id):

 

    bills = GeneralBuying.objects.filter(pk=id)
   

    bill_instance = get_object_or_404(GeneralBuying,pk=id )

    clint = bill_instance.client.pk


    user_id = bill_instance.created_by.id
    records = GeneralInner.objects.filter(general_buying= id)
    user = CustomUser.objects.filter(pk =user_id)
    return render(request, 'inner/view.html', {'form': bills , 'form_in' :records  ,  'user' : user})







# List all Buying Types
def buying_type_list(request):
    buying_types = BuyingType.objects.all()
    return render(request, 'buyingtype/list.html', {'buying_types': buying_types})

# Create a new Buying Type
def buying_type_create(request):
    if request.method == 'POST':
        form = BuyingTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buying_type_list')
    else:
        form = BuyingTypeForm()

    return render(request, 'buyingtype/new.html', {'form': form, 'title': 'Add New Buying Type'})



@login_required

def buying_type_update(request, pk):
    buying_type = get_object_or_404(BuyingType, pk=pk)
    if request.method == 'POST':
        form = BuyingTypeForm(request.POST, instance=buying_type)
        if form.is_valid():
            form.save()
            return redirect('buying_type_list')
    else:
        form = BuyingTypeForm(instance=buying_type)

    return render(request, 'buyingtype/new.html', {'form': form, 'title': 'Edit Buying Type'})



@login_required
# Delete a Buying Type
def buying_type_delete(request, pk):
    buying_type = get_object_or_404(BuyingType, pk=pk)
    if request.method == 'POST':
        buying_type.delete()
        return redirect('buying_type_list')
    
    return render(request, 'buyingtype/delete.html', {'buying_type': buying_type})



@login_required
def buying_jar(request, pk):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    jar_inners = JarInner.objects.filter(general_buying=pk)
 

    if request.method == 'POST':
        form = JarInnerForm(request.POST)
        if form.is_valid():
            jar_inner = form.save(commit=False)
            jar_inner.general_buying = general_buying  # Set general_buying automatically
            jar_inner.save()
            messages.success(request, 'Jar Inner record added successfully.')
            return redirect('buying_jar', pk=general_buying.pk)
        else:
            messages.error(request, 'There was an error adding the Jar Inner record. Please check the form.')
    else:
        form = JarInnerForm()

    context = {
        'general_buying': general_buying,
        'jar_inners': jar_inners,
        'form': form,  # Form for adding a new JarInner
    }

    return render(request, 'JarInner/form.html', context)



@login_required
def delete_jar_innner(request, pk ,id):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    jar_inners = get_object_or_404(JarInner,pk=id)
    jar_inners.delete()

    

   
    messages.success(request, 'Jar Inner record deleted successfully.')
    return redirect('buying_jar', pk=general_buying.pk)



    



@login_required
def buying_jar_off(request, pk):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    jar_inners = Jar_off_Inner.objects.filter(general_buying=pk)
    if request.method == 'POST':
        form = Jar_off_InnerForm(request.POST)
        if form.is_valid():
            jar_inner = form.save(commit=False)
            jar_inner.general_buying = general_buying  # Set general_buying automatically
            jar_inner.save()
            messages.success(request, 'Jar of  Inner record added successfully.')
            return redirect('buying_jar_off', pk=general_buying.pk)
        else:
            messages.error(request, 'There was an error adding the Jar Inner record. Please check the form.')
    else:
        form = Jar_off_InnerForm()

    context = {
        'general_buying': general_buying,
        'jar_inners': jar_inners,
        'form': form,  # Form for adding a new JarInner
    }

    return render(request, 'Jar_off_Inner/form.html', context)





@login_required
def delete_jar_off_innner(request, pk ,id):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    jar_inners = get_object_or_404(Jar_off_Inner,pk=id)
    jar_inners.delete()
    
    messages.success(request, 'Jar Inner record deleted successfully.')

    return redirect('buying_jar_off', pk=general_buying.pk)

    










@login_required
def buying_pakage(request, pk):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    jar_inners = PakageInner.objects.filter(general_buying=pk)
    if request.method == 'POST':
        form = PakageInnerForm(request.POST)
        if form.is_valid():
            jar_inner = form.save(commit=False)
            jar_inner.general_buying = general_buying  # Set general_buying automatically
            jar_inner.save()
            messages.success(request, 'Jar of  Inner record added successfully.')
            return redirect('buying_pakage', pk=general_buying.pk)
        else:
            messages.error(request, 'There was an error adding the Jar Inner record. Please check the form.')
    else:
        form = PakageInnerForm()

    context = {
        'general_buying': general_buying,
        'jar_inners': jar_inners,
        'form': form,  # Form for adding a new JarInner
    }

    return render(request, 'pakage_inner/form.html', context)



@login_required

def delete_pakage_inner(request, pk ,id):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)
    jar_inners = get_object_or_404(PakageInner,pk=id)
    jar_inners.delete()
    messages.success(request, 'Jar Inner record deleted successfully.')

    return redirect('buying_pakage', pk=general_buying.pk)

    

@login_required

def material_list(request):
    materials = Material.objects.all()
    return render(request, 'materials/list.html', {'materials': materials})

@login_required
def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material-list')  # Redirect to the material list
    else:
        form = MaterialForm()
    return render(request, 'materials/form.html', {'form': form})


@login_required
def material_edit(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('material-list')  # Redirect to the material list
    else:
        form = MaterialForm(instance=material)
    return render(request, 'materials/form.html', {'form': form})



@login_required

def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('material-list')
    
@login_required
def raw_materials_list(request):
    raw_materials = RawMaterials.objects.all()
    return render(request, 'raw_materials/list.html', {'raw_materials': raw_materials})






@login_required
# View to insert a new raw material
def add_raw_material(request):
    if request.method == 'POST':
        form = RawMaterialsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('raw_materials_list')  # Redirect to the list after adding
    else:
        form = RawMaterialsForm()
    return render(request, 'raw_materials/form.html', {'form': form})




@login_required

# View for updating an existing RawMaterial
def raw_material_update(request, pk):
    raw_material = get_object_or_404(RawMaterials, pk=pk)

    if request.method == 'POST':
        form = RawMaterialsForm(request.POST, instance=raw_material)
        if form.is_valid():
            form.save()
            messages.success(request, "Raw material updated successfully!")
            return redirect('raw_materials_list')
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = RawMaterialsForm(instance=raw_material)

    return render(request, 'raw_materials/form.html', {'form': form, 'raw_material': raw_material})



@login_required
# View for deleting a RawMaterial
def raw_material_delete(request, pk):
    raw_material = get_object_or_404(RawMaterials, pk=pk)
    if request.method == 'POST':
        raw_material.delete()
        messages.success(request, "Raw material deleted successfully!")
        return redirect('raw_materials_list')















@login_required
def buying_Rawmaterials(request, pk):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)
    jar_inners = RawmaterialsInner.objects.filter(general_buying=general_buying)

    if request.method == 'POST':
        form = RawmaterialsInnerForm(request.POST)
        if form.is_valid():
            jar_inner = form.save(commit=False)
            jar_inner.general_buying = general_buying  # Set general_buying automatically
            jar_inner.save()
            messages.success(request, 'Raw materials record added successfully.')
            return redirect('buying_Rawmaterials', pk=general_buying.pk)
        else:
            messages.error(request, 'There was an error adding the raw materials record. Please check the form.')
    else:
        form = RawmaterialsInnerForm()

    context = {
        'general_buying': general_buying,
        'jar_inners': jar_inners,
        'form': form,
    }

    return render(request, 'rawmaterials/form.html', context)








@login_required
def delete_Rawmaterials(request, pk ,id):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    inners = get_object_or_404(RawmaterialsInner,pk=id)
    inners.delete()
    messages.success(request, 'Raw Inner record deleted successfully.')

    return redirect('buying_Rawmaterials', pk=general_buying.pk)









@login_required

def Factor_materials_list(request):
    raw_materials = FactoryMaterials.objects.all()
    return render(request, 'Factor_materials/list.html', {'raw_materials': raw_materials})






@login_required
# View to insert a new raw material
def add_Factor_material(request):
    if request.method == 'POST':
        form = FactoryMaterialsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('raw_materials_list')  # Redirect to the list after adding
    else:
        form = FactoryMaterialsForm()
    return render(request, 'Factor_materials/form.html', {'form': form})




@login_required

# View for updating an existing RawMaterial
def Factor_material_update(request, pk):
    raw_material = get_object_or_404(FactoryMaterials, pk=pk)

    if request.method == 'POST':
        form = FactoryMaterialsForm(request.POST, instance=raw_material)
        if form.is_valid():
            form.save()
            messages.success(request, "Raw material updated successfully!")
            return redirect('Factor_materials_list')
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = FactoryMaterialsForm(instance=raw_material)

    return render(request, 'Factor_materials/form.html', {'form': form, 'raw_material': raw_material})



@login_required
# View for deleting a RawMaterial
def Factor_material_delete(request, pk):
    raw_material = get_object_or_404(FactoryMaterials, pk=pk)
    if request.method == 'POST':
        raw_material.delete()
        messages.success(request, "Factor material deleted successfully!")
        return redirect('Factor_materials_list')






@login_required

def buying_Factormaterials(request, pk):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)
    jar_inners = FacoryMaterialsInner.objects.filter(general_buying=general_buying)

    if request.method == 'POST':
        form = FacoryMaterialsInnerForm(request.POST)
        if form.is_valid():
            jar_inner = form.save(commit=False)
            jar_inner.general_buying = general_buying  # Set general_buying automatically
            jar_inner.save()
            messages.success(request, 'Facory materials record added successfully.')
            return redirect('buying_Factormaterials', pk=general_buying.pk)
        else:
            messages.error(request, 'There was an error adding the Facory materials record. Please check the form.')
    else:
        form = FacoryMaterialsInnerForm()

    context = {
        'general_buying': general_buying,
        'jar_inners': jar_inners,
        'form': form,
    }

    return render(request, 'Facorymaterialsinner/form.html', context)







@login_required

def delete_Facorymaterials(request, pk ,id):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    inners = get_object_or_404(FacoryMaterialsInner,pk=id)
    inners.delete()
    
    messages.success(request, 'Raw Inner record deleted successfully.')

    return redirect('buying_Factormaterials', pk=general_buying.pk)



from django.http import JsonResponse
from django.db.models import Q
from .models import Assets

@login_required
def assets_list_json(request):
    query = request.GET.get('q', '')  # Get the search query
    if query:
        assets = Assets.objects.filter(Q(name__icontains=query))
    else:
        assets = Assets.objects.all()

    data = [
        {
            'id': asset.id,
            'name': asset.name,
            'stock': float(asset.stock),
            'price': float(asset.price),
            'adjustment': asset.adjustment,
        }
        for asset in assets
    ]
    return JsonResponse(data, safe=False)




def assets_list_view(request):
    return render(request, 'Assets/list.html')







@login_required
def Asstes_create(request):
    if request.method == 'POST':
        form = AssetsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assets-list')  # Redirect to the material list
    else:
        form = AssetsForm()
    return render(request, 'Assets/form.html', {'form': form})




@login_required
def Asstes_edit(request, pk):
    material = get_object_or_404(Assets, pk=pk)
    if request.method == 'POST':
        form = AssetsForm(request.POST, request.FILES, instance=material)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'edited Asstes record  successfully.')
            return redirect('assets-list')  # Redirect to the material list
    else:
        form = AssetsForm(instance=material)
    return render(request, 'Assets/form.html', {'form': form, 'material': material})



@login_required

def Asstes_delete(request, pk):
    inners = get_object_or_404(Assets,pk=pk)
    inners.delete()
    
    messages.success(request, 'Asstes record deleted successfully.')
    return redirect('assets-list')









@login_required
def buying_assets_inner(request, pk):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)
    iner = AssetsInner.objects.filter(general_buying=general_buying)

    if request.method == 'POST':
        form = assetsInnerForm(request.POST)
        if form.is_valid():
            jar_inner = form.save(commit=False)
            jar_inner.general_buying = general_buying  # Set general_buying automatically
            jar_inner.save()
            messages.success(request, ' assets record added successfully.')
            return redirect('buying_assets_inner', pk=general_buying.pk)
        else:
            messages.error(request, 'There was an error adding the record. Please check the form.')
    else:
        form = assetsInnerForm()

    context = {
        'general_buying': general_buying,
        'jar_inners': iner,
        'form': form,
    }

    return render(request, 'Assets/buye.html', context)



@login_required

def delete_assets(request, pk ,id):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    inners = get_object_or_404(AssetsInner,pk=id)
    inners.delete()
    
    messages.success(request, 'Raw Inner record deleted successfully.')

    return redirect('buying_assets_inner', pk=general_buying.pk)






@login_required

def makePyment(request,id):
    general_buying = get_object_or_404(GeneralBuying, pk=id)
    if not general_buying.is_pyed:


        general_payment = ClintPayment.objects.create(
                    amount=general_buying.price,
                    clint=general_buying.client,
            
                    source=MoneySource.objects.filter(source_type='cash').first()

                )
        general_payment.save()
        messages.success(request, ' pyment done   successfully. ')
        general_buying.is_pyed = True
        general_buying.save()
        return redirect('general_buying_list')
    else :
         messages.success(request, ' pyment alredy is  done   successfully. ')
    return redirect('general_buying_list')





    if request.method == 'POST':
        form = ClintPymantForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.clint = clint
            payment.save()


@login_required


def create_clint_payment(request , id):
    general_buying = get_object_or_404(GeneralBuying, pk=id)

    note = f"{general_buying}  Total Amount : {general_buying.price } ₺ on :  {general_buying.created_at}  bill id : {general_buying.pk} "
    initial_data = {'amount': general_buying.price  , 'note':note} 
    if request.method == 'POST':
        form = ClintPymantForm(request.POST, request.FILES)
        
        if form.is_valid():
            payment = form.save(commit=False)
            payment.clint = general_buying.client
            payment.save()
            messages.success(request, 'Payment has been successfully recorded.   {general_buying.client}')
            general_buying.is_pyed = True

            general_buying.save()
            return redirect('general_buying_list')  # Replace with the name of your payment list view or desired URL
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClintPymantForm(initial=initial_data)

    return render(request, 'clint/payment_form.html', {'form': form})





@login_required


def create_clint_payment_add(request , id):
    clint = get_object_or_404(clints,pk=id)
    

  

    if request.method == 'POST':
        form = ClintPymantForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.clint = clint
            record.save()
       
         
            messages.success(request, 'Payment has been successfully recorded.')
    
            return redirect('general_buying_list')  # Replace with the name of your payment list view or desired URL
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClintPymantForm()

    return render(request, 'clint_payment_form.html', {'form': form})






@login_required
# here is for the user to fatch the amount of 
def raw_materials_summary(request):
    # Initialize start and end dates
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    results = []
    if start_date and end_date:
        try:
            # Parse the dates
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Query the database
            results = RawmaterialsInner.objects.filter(
                created_at__range=(start_date, end_date)
            ).values(
                'RawMaterials__product_name'
            ).annotate(
                total_amount=Sum('amount'),
                total_price=Sum('total')
            )

        except ValueError:
            # Handle invalid date format
            results = []

    context = {
        'results': results,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'rawmaterials/summary.html', context)






@login_required
# here is for the user to fatch the amount of 
def factory_materials_summary(request):
    # Initialize start and end dates
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    results = []
    if start_date and end_date:
        try:
            # Parse the dates
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Query the database
            results = FacoryMaterialsInner.objects.filter(
                created_at__range=(start_date, end_date)
            ).values(
                'RawMaterials__product_name'
            ).annotate(
                total_amount=Sum('amount'),
                total_price=Sum('total')
            )

        except ValueError:
            # Handle invalid date format
            results = []

    context = {
        'results': results,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'rawmaterials/summary.html', context)










@login_required
def buying_Spendes_inner(request, pk):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)
    iner = Spendes.objects.filter(general_buying=general_buying)

    if request.method == 'POST':
        form = spendesInnerForm(request.POST)
        if form.is_valid():
            jar_inner = form.save(commit=False)
            jar_inner.general_buying = general_buying  # Set general_buying automatically
            jar_inner.save()
            messages.success(request, ' assets record added successfully.')
            return redirect('buying_Spendes_inner', pk=general_buying.pk)
        else:
            messages.error(request, 'There was an error adding the record. Please check the form.')
    else:
        form = spendesInnerForm()

    context = {
        'general_buying': general_buying,
        'jar_inners': iner,
        'form': form,
    }

    return render(request, 'spened/buye.html', context)





@login_required

def delete_spendes(request, pk ,id):
    general_buying = get_object_or_404(GeneralBuying, pk=pk)

    inners = get_object_or_404(Spendes,pk=id)
    inners.delete()
    
    messages.success(request, 'spendes Inner record deleted successfully.')

    return redirect('buying_Spendes_inner', pk=general_buying.pk)

