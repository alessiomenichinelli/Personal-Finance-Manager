from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        string = self.name
        string = string[0].upper() + string[1:]
        return string

    def calculate(self):
        balance = 0
        expenses = Expense.objects.filter(user=self.user, account=self)
        incomes = Income.objects.filter(user=self.user, account=self)
        for ex in expenses:
            balance -= ex.amount
        for inc in incomes:
            balance += inc.amount
        balance = str(balance)
        balance += '€'
        return balance

class Payment_Method(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        string = self.name
        string = string[0].upper() + string[1:]
        return string
    
    def calculate(self):
        balance = 0
        expenses = Expense.objects.filter(user=self.user, payment_method=self)
        incomes = Income.objects.filter(user=self.user, payment_method=self)
        for ex in expenses:
            balance -= ex.amount
        for inc in incomes:
            balance += inc.amount
        balance = str(balance)
        balance += '€'
        return balance

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        string = self.name
        string = string[0].upper() + string[1:]
        return string
    
    def calculate(self):
        balance = 0
        expenses = Expense.objects.filter(user=self.user, category=self)
        for ex in expenses:
            balance -= ex.amount
        balance = str(balance)
        balance += '€'
        return balance

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(Payment_Method, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits = 6, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.date) + "_" + str(self.amount) + "(" + str(self.user.id) + ")" + "(" + str(self.id) + ")"
    
    def expense_user_id(self, id):
        if(self.user.id == id):
                return True
        return False
    
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(Payment_Method, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits = 6, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.date) + "_" + str(self.amount) + "(" + str(self.user.id) + ")" + "(" + str(self.id) + ")"
    
    def income_user_id(self, id):
        if(self.user.id == id):
                return True
        return False
