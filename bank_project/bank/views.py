from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, DepositForm, WithdrawForm
from .models import UserAccount
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'bank/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'bank/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    try:
        account = UserAccount.objects.get(user=request.user)
    except UserAccount.DoesNotExist:
        messages.error(request, 'Your account details are missing. Please contact support.')
        return redirect('logout')  # Or another appropriate action
    return render(request, 'bank/home.html', {'account': account})

@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = UserAccount.objects.get(user=request.user)
            account.deposit(amount)
            messages.success(request, f'Amount ${amount} deposited successfully.')
            return redirect('home')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form})

@login_required
def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            pin = form.cleaned_data['pin']
            account = UserAccount.objects.get(user=request.user)
            if pin != account.pin:
                messages.error(request, 'Invalid PIN.')
            else:
                if account.withdraw(amount):
                    messages.success(request, f'Amount ${amount} withdrawn successfully.')
                    return redirect('home')
                else:
                    messages.error(request, 'Insufficient balance.')
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form})
