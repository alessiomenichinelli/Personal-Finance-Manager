from rest_framework import serializers

from .models import User, Account, Category, Payment_Method, Expense, Income

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AccountSerializers(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    
    class Meta:
        model = Account
        fields = '__all__'

class PMSerializers(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()
    class Meta:
        model = Payment_Method
        fields = '__all__'

class CategorySerializers(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = '__all__'

class ExpenseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class IncomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'