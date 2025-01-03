# forms.py
from django import forms
from .models import Employee , Salary , EmployeePayment

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'age', 'tc', 'title', 'state', 'is_working' , 'phone' , 'phone_2']  # Specify which fields you want in the form
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ادخل الاسم'}),
            'position': forms.TextInput(attrs={'placeholder': 'ادخل الوظيفة'}),
            'age': forms.NumberInput(attrs={'placeholder': 'العمر'}),
            'tc': forms.TextInput(attrs={'placeholder': 'رقم الهوية'}),
            'title': forms.TextInput(attrs={'placeholder': 'اللقب'}),
            'state': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'activeCheck'}),
            'is_working': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'activeCheck'}),
             'phone': forms.TextInput(attrs={'placeholder': 'رقم الهاتف'}),
             'phone_2': forms.TextInput(attrs={'placeholder': 'رقم الطوارئ'}),
             
                # Example for checkbox input with custom class
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})




class TCForm(forms.Form):
    tc = forms.CharField(
        max_length=100,
        required=True,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control pl-3',
            'placeholder': 'Search'
        })
    )


class MarkPaidForm(forms.Form):
    number_of_records = forms.IntegerField(label='Number of Records to Mark as Paid')



class ChatForm(forms.Form):
    user_input = forms.CharField(label='Your message', max_length=1000, widget=forms.Textarea)



class AnalysisForm(forms.Form):
    question = forms.CharField(label='Question', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your question here'}))







class SalaryForm(forms.ModelForm):
     class Meta:
        model = Salary
        fields = [ 'amount' , "effective_date"]
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
        }

  


class EmployeePaymentForm(forms.ModelForm):
    class Meta:
        model = EmployeePayment
        fields = ['amount', 'date', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})