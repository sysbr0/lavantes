# forms.py
from django import forms
from .models import *
from clints.models import *

class ClintsForm(forms.ModelForm):
 class Meta:
        model = clints
        fields = [
            'name', 'email', 'number', 'address', 'profile_image', "company"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter client name' , 'class': 'form-control custom-width' }),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter client email' , 'class': 'form-control custom-width' }),
            'number': forms.TextInput(attrs={'placeholder': 'Enter contact number' , 'class': 'form-control custom-width' }),
            'address': forms.TextInput(attrs={'placeholder': 'Enter client source' , 'class': 'form-control custom-width custom-hight' }),
            'profile_image': forms.ClearableFileInput(attrs={ 'class': 'form-control custom-width' }),
             'company': forms.TextInput(attrs={'placeholder': 'Enter company name' , 'class': 'form-control custom-width ' }),

              }



class GeneralBuyingForm(forms.ModelForm):
    class Meta:
        model = GeneralBuying
        fields = ['client', 'buying_type', 'created_at' , 'notee']
        widgets = {
             'buying_type': forms.Select(attrs={'class': 'form-control'}),
             'client': forms.Select(attrs={'class': 'form-control'}),
             'created_at':forms.DateTimeInput(attrs={ 'class': 'form-control','placeholder': 'Enter date and time','type': 'datetime-local'  # Use 'datetime-local' for modern HTML5 browsers
                }
            ),
             'notee': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Note'})}




class GeneralInnerForm(forms.ModelForm):
    class Meta:
        model = GeneralInner
        fields = ['description', 'price', 'amount', 'note']




class BuyingTypeForm(forms.ModelForm):
    class Meta:
        model = BuyingType
        fields = ['name', 'Name_En']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'Name_En': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter English name'}),
        }

class JarInnerForm(forms.ModelForm):
      class Meta:
        model = JarInner
        fields = ['jar', 'amount', 'price', 'note']  # Removed 'general_buying' field
        widgets = {
            'jar': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
        }




class Jar_off_InnerForm(forms.ModelForm):
    class Meta:
        model = Jar_off_Inner  # Define the model that this form is associated with
        fields = ['jar_of', 'amount', 'price', 'note', 'created_at']  # List of fields to include in the form
        widgets = {
            'jar_of': forms.Select(attrs={'class': 'form-control'}),  # Widget for the 'jar_of' field
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),  # Widget for the 'amount' field
            'price': forms.NumberInput(attrs={'class': 'form-control'}),  # Widget for the 'price' field
            'note': forms.TextInput(attrs={'class': 'form-control'}),  # Widget for the 'note' field
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Widget for 'created_at' field
        }

   


class PakageInnerForm(forms.ModelForm):
    class Meta:
        model = PakageInner  # Define the model that this form is associated with
        fields = ['pakage', 'amount', 'price', 'note', 'created_at']  # List of fields to include in the form
        widgets = {
            'pakage': forms.Select(attrs={'class': 'form-control'}),  # Widget for the 'jar_of' field
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),  # Widget for the 'amount' field
            'price': forms.NumberInput(attrs={'class': 'form-control'}),  # Widget for the 'price' field
            'note': forms.TextInput(attrs={'class': 'form-control'}),  # Widget for the 'note' field
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Widget for 'created_at' field
        }






class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['product_name', 'stock', 'price', 'adjustment']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'adjustment': forms.NumberInput(attrs={'class': 'form-control'}),
        }





class RawMaterialsForm(forms.ModelForm):
    class Meta:
        model = RawMaterials  # Specify the model
        fields = ['product_name', 'Materials', 'WaistPercentage', 'stock', 'price', 'adjustment']  # Specify the fields
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Materials': forms.Select(attrs={'class': 'form-control'}),
            'WaistPercentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'adjustment': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class RawmaterialsInnerForm(forms.ModelForm):
    class Meta:
        model = RawmaterialsInner
        fields = ['RawMaterials', 'amount', 'price', 'note']
        widgets = {
            'RawMaterials': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
          
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['RawMaterials'].queryset = RawMaterials.objects.all()  # Populate RawMaterials



class FactoryMaterialsForm(forms.ModelForm):
    class Meta:
        model = FactoryMaterials  # Specify the model
        fields = ['product_name', 'Materials', 'WaistPercentage', 'stock', 'price', 'adjustment']  # Specify the fields
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Materials': forms.Select(attrs={'class': 'form-control'}),
            'WaistPercentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'adjustment': forms.NumberInput(attrs={'class': 'form-control'}),
        }



    
class FacoryMaterialsInnerForm(forms.ModelForm):
    class Meta:
        model = FacoryMaterialsInner
        fields = ['RawMaterials', 'amount', 'price', 'note']
        widgets = {
            'RawMaterials': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),

        }

  




class AssetsForm(forms.ModelForm):
    class Meta:
        model = Assets
        fields = ['name', 'stock', 'price', 'adjustment' , 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'adjustment': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }




    
class assetsInnerForm(forms.ModelForm):
    class Meta:
        model = AssetsInner
        fields = ['product', 'amount', 'price', 'note']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),

        }


    
class spendesInnerForm(forms.ModelForm):
    class Meta:
        model = Spendes
        fields = [ 'amount', 'price', 'note','buying_type']
        widgets = {
           
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
              'buying_type': forms.Select(attrs={'class': 'form-control'}),

        }

 

  



