from django import forms
from .models import *
from django.forms import inlineformset_factory



class JarForm(forms.ModelForm):
    class Meta:
        model = Jar
        fields = [
            'jar_name', 'image'
        ]
        widgets = {
            'jar_name': forms.TextInput(attrs={'placeholder': 'Enter jar name'}),

            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }

#            'clint_tex': forms.NumberInput(attrs={'placeholder': 'Enter client tax'}),

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            'package_name','package_arabic', 'image'
        ]
        widgets = {
            'package_name': forms.TextInput(attrs={'placeholder': 'Enter bakge name'}),
            'package_arabic': forms.TextInput(attrs={'placeholder': 'Enter bakge name AR '}),

            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }


class ProductHamForm(forms.ModelForm):
    class Meta:
        model = ProductHam
        fields = [
            'product_name','top', 'percentage', 'image'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter bakge name'}),
            'top' : forms.NumberInput(attrs={'placeholder': 'Enter the  max kg '}),
            'percentage' : forms.NumberInput(attrs={'placeholder': 'production cost %'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
        }


class MainProductForm(forms.ModelForm):
    class Meta:
        model = MainProduct
        fields = [
            'product_name', 'product_type', 'product_ham', 'jar', 'package', 
            'image', 'net_weight', 'top_weight', 'amount_inside', 'qr'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'product_type': forms.TextInput(attrs={'placeholder': 'Enter product type'}),
            'product_ham': forms.Select(attrs={'class': 'form-control'}),
            'jar': forms.Select(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter image URL'}),
            'net_weight': forms.NumberInput(attrs={'placeholder': 'Enter the net weight'}),
            'top_weight': forms.NumberInput(attrs={'placeholder': 'Enter the top weight'}),
            'amount_inside': forms.NumberInput(attrs={'placeholder': 'Enter the amount inside'}),
            'qr': forms.NumberInput(attrs={'placeholder': 'Enter product QR'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MainProductForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['product_ham'].queryset = ProductHam.objects.filter(created_by=user.id)
            self.fields['jar'].queryset = Jar.objects.filter(created_by=user.id)
            self.fields['package'].queryset = Package.objects.filter(created_by=user.id)









class UdsBill_Form(forms.ModelForm):
    class Meta:
        model = UdsBills
        fields = ['customer', 'note']  # Include only the fields you want
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a note'}),
        }
        # Define the form field attributes
        # The `customer` field is required by default as it's a ForeignKey

    def __init__(self, *args, **kwargs):
        super(UdsBill_Form, self).__init__(*args, **kwargs)
        self.fields['note'].required = False






class TrBill_Form(forms.ModelForm):
    class Meta:
        model = TrBills
        fields = ['customer', 'note']  # Include only the fields you want
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a note'}),
        }
        # Define the form field attributes
        # The `customer` field is required by default as it's a ForeignKey

    def __init__(self, *args, **kwargs):
        super(TrBill_Form, self).__init__(*args, **kwargs)
        self.fields['note'].required = False






UdsBillInnerFormSet = inlineformset_factory(
    UdsBills,
    UdsBill_inner,
    fields=['main_product', 'amount', 'price', 'note'],
    extra=0,
    can_delete=True
)






class UdsBillForm(forms.ModelForm):
    class Meta:
        model = UdsBills
        fields = ['customer', 'note', 'is_paid']


class UdsBillInnerForm(forms.ModelForm):
    class Meta:
        model = UdsBill_inner
        fields = [ 'amount', 'price', 'note', 'main_product' , 'id']
        widgets = {
            'note': forms.Textarea(attrs={ 'placeholder': 'NOTE',
                'class': 'note-field',  # Custom class for styling
             
            }),

             'amount': forms.NumberInput(attrs={'placeholder': 'AMOUNT'}),


             
             'price': forms.NumberInput(attrs={'placeholder': 'PRICE'}),
             'main_product': forms.Select(attrs={'placeholder': 'Select Main Product'}),  # Placeholder for main_product


        }





TrBillInnerFormSet = inlineformset_factory(
    TrBills,
    TrBill_inner,
    fields=['main_product', 'amount', 'price', 'note'],
    extra=0,
    can_delete=True
)






class TrBillForm(forms.ModelForm):
    class Meta:
        model = TrBills
        fields = ['customer', 'note', 'is_paid']


class TrBillInnerForm(forms.ModelForm):
    class Meta:
        model = TrBill_inner
        fields = [ 'amount', 'price', 'note', 'main_product' , 'id']
        widgets = {
            'note': forms.Textarea(attrs={ 'placeholder': 'NOTE',
                'class': 'note-field',  # Custom class for styling
             
            }),

             'amount': forms.NumberInput(attrs={'placeholder': 'AMOUNT'}),


             
             'price': forms.NumberInput(attrs={'placeholder': 'PRICE'}),
             'main_product': forms.Select(attrs={'placeholder': 'Select Main Product'}),  # Placeholder for main_product


        }
