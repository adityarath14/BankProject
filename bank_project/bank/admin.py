# bank/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserAccount
from bank.models import*

# Define an inline admin descriptor for UserAccount model
class UserAccountInline(admin.StackedInline):
    model = UserAccount
    can_delete = False
    verbose_name_plural = 'UserAccount'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserAccountInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserAccount)

