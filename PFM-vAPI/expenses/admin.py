from django.contrib import admin

from .models import Account, Category, Payment_Method, Expense, Income

admin.site.register(Account)
admin.site.register(Payment_Method)
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(Income)