# forms.py
from django import forms
from .models import *

class CostomersForm(forms.ModelForm):
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










class ChangePasswordForm(forms.Form):
    token = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter new Password'}),
        label='New Token',
        required=True
    )
    confirm_token = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter new Password'}),
        label='Confirm Token',
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        token = cleaned_data.get('token')
        confirm_token = cleaned_data.get('confirm_token')

        if token and confirm_token and token != confirm_token:
            raise forms.ValidationError('Tokens do not match')

        return cleaned_data




    









class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = clints
        fields = ['profile_image', 'name', 'tex', 'email', 'number', 'address',
            'is_company', 'company',]

        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
             'name': forms.TextInput(attrs={'placeholder': 'Enter Costomer name' , 'class': 'custom-width font_size'  }),
             'tex': forms.NumberInput(attrs={'placeholder': 'Enter tax', 'class': 'custom-width font_size'}),   
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'class': 'custom-width font_size'}),
            'number': forms.TextInput(attrs={'placeholder': 'Enter contact number','class': 'custom-width font_size'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter address' , 'class': 'custom-width  custom-hight'}),
            'is_company': forms.CheckboxInput(attrs={'placeholder': 'Is it a company?' , 'class': 'custom-width font_size '}),
            'company': forms.Textarea(attrs={'placeholder': 'Enter company name' , 'class': 'custom-width  custom-hight'}),



        }

class CostomersFormAdvanv(forms.ModelForm):
    class Meta:
        model = clints
        fields = [
            'name', 'tex', 'email', 'number', 'address',
            'is_company', 'company',  'profile_image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name'}),
            'tex': forms.NumberInput(attrs={'placeholder': 'Enter tax'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'number': forms.TextInput(attrs={'placeholder': 'Enter contact number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
            'is_company': forms.CheckboxInput(attrs={'placeholder': 'Is it a company?'}),
            'company': forms.TextInput(attrs={'placeholder': 'Enter company name'}),
      
            'token': forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background-color: lightgray;'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super(CostomersFormAdvanv, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CostomersFormAdvanv, self).save(commit=False)
        # Generate token if it's not provided
        if not instance.token:
            instance.generate_token()  # Replace with your token generation logic
        if commit:
            instance.save()
        return instance
    



    




   

class ClintPymantForm(forms.ModelForm):
    class Meta:
        model = ClintPayment
        fields = ('source', 'amount', 'date', 'note', 'image')
        widgets = {
            'source': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter date and time', 'type': 'datetime-local'}
            ),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Note'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

