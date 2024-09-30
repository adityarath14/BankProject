# bank/forms.py

from django import forms
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(max_length=15, required=True)
    aadhar_number = forms.CharField(max_length=12, required=True)
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'aadhar_number', 'pin', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.useraccount.mobile_number = self.cleaned_data['mobile_number']
            user.useraccount.aadhar_number = self.cleaned_data['aadhar_number']
            user.useraccount.pin = self.cleaned_data['pin']
            user.useraccount.save()
        return user

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        label='Amount to Deposit'
    )

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        label='Amount to Withdraw'
    )
    pin = forms.CharField(
        max_length=4, 
        widget=forms.PasswordInput, 
        label='Enter PIN'
    )
