from django import forms
from .models import *
from datetime import datetime
from django.forms import PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class PaymentForm(forms.Form):
    card_number = forms.CharField()
    date = forms.CharField()
    cvc = forms.CharField()
    sum = forms.IntegerField()

    def clean(self):
        form_data = self.cleaned_data

        if 'sum' not in form_data or form_data['sum'] <= 0:
            self._errors["sum"] = ["Invalid sum"]
            return form_data
    
        if 'date' not in form_data or not form_data['date'].strip()[-2:].isdigit() or not form_data['date'].strip()[:2].isdigit():
            self._errors["date"] = ["Card is expired"]
            return form_data
    
        year = int(form_data['date'].strip()[-2:])
        month = int(form_data['date'].strip()[:2])
        if year and (year < datetime.now().year % 100):
            self._errors["date"] = ["Card is expired"]
            return form_data
        if month and month < datetime.now().month:
            self._errors["date"] = ["Card is expired"]
            return form_data

        if 'cvc' not in form_data or (len(form_data['cvc']) != 3):
            self._errors["cvc"] = ["Invalid cvc"]
            return form_data

        if 'card_number' not in form_data or (len(form_data['card_number']) != 16 and len(form_data['card_number']) != 13):
            self._errors["card_number"] = ["Invalid card number"]
            return form_data

        card_number = int(form_data['card_number'].strip()[:4])
        # check visa
        if (card_number // 1000 == 4):
            return form_data
    
        # check mastercard
        if len(form_data['card_number']) == 16 and (51 <= int(str(card_number[:2])) <= 55):        
            return form_data

        # check МИР
        if len(form_data['card_number']) == 16 and (2200 <= card_number <= 2204):
            return form_data

        self._errors["card_number"] = ["Invalid card number"]
        return form_data

class UserFormCustom(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'password']
        widgets = {
            'password': PasswordInput
        }

        
class UserRegistration(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
    class Meta:
        model=User
        fields=['email','username','password1','password2',]
        widgets = {
        'email': forms.EmailInput(attrs={'class': 'email-field'}),
        'username': forms.TextInput(attrs={'class': 'username-field'}),

        'password2': forms.PasswordInput(attrs={'class': 'password-field'})
        }
        help_text = {
            'password': '',
            'username': None,
            'email': None,
        }
          
class UserEdit(forms.ModelForm):
    avatar_field=forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        super(UserEdit, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = None
        self.fields['username'].help_text = None
    class Meta:
        model=User
        
        fields= ['email','username','first_name','last_name',]
        help_text = {
            'password': '',
            'username': None,
            'email': None,
            
        }
        error_messages = {
            'email': None,
        }
        


class PurchaseForm(forms.Form):
    stock_quantity = forms.IntegerField()

    def clean(self):
        form_data = self.cleaned_data

        if 'stock_quantity' not in form_data or form_data['stock_quantity'] <= 0:
            self._errors["stock_quantity"] = ["Некорректное количество"]
            return form_data


        return form_data
