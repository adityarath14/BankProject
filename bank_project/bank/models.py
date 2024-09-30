# bank/models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='useraccount')
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pin = models.CharField(max_length=128, blank=True, null=True)  # Increased length for hashed PIN

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)
        self.save()

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username}'s Account"
