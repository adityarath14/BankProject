# bank/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserAccount

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        # Skip creating UserAccount for superusers to avoid duplicate aadhar_number
        if not instance.is_superuser:
            UserAccount.objects.create(
                user=instance,
                mobile_number='0000000000',       # Placeholder: Replace with actual data or handle accordingly
                aadhar_number='000000000000',     # Placeholder: Replace with actual data or handle accordingly
                balance=0.00,
                pin='0000'                         # Placeholder: Replace with actual data or handle securely
            )

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    if hasattr(instance, 'useraccount'):
        instance.useraccount.save()
