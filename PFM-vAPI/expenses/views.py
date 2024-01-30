from django.shortcuts import render, get_object_or_404

from .models import Account, Category, Payment_Method, Expense, Income
from .serializer import UserSerializers, AccountSerializers, PMSerializers, CategorySerializers, ExpenseSerializers, IncomeSerializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class LoginAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'id': user.id, 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CategoryListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        limit = request.query_params.get('limit', None)
        if limit:
            categories = Category.objects.filter(user=self.request.user)[:int(limit)]
        else:
            categories = Category.objects.filter(user=self.request.user)
        for category in categories:
            category.balance = category.calculate()
        serializer = CategorySerializers(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = self.request.data.copy()
        data['user'] = self.request.user.pk
        serializer = CategorySerializers(data=data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, pk, format=None):
        category = get_object_or_404(Category, user=self.request.user, pk=pk)
        category.balance = category.calculate()
        serializer = CategorySerializers(category)
        return Response(serializer.data)    

    def put(self, request, pk, format=None):
        if pk != request.data["id"]:
            raise Http404
        category = get_object_or_404(Category, user=self.request.user, pk=pk)
        serializer = CategorySerializers(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = get_object_or_404(Category, user=self.request.user, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AccountListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        accounts = Account.objects.filter(user=self.request.user)
        for account in accounts:
            account.balance = account.calculate()
        serializer = AccountSerializers(accounts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = self.request.data.copy()
        data['user'] = self.request.user.pk
        serializer = AccountSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, pk, format=None):
        account = get_object_or_404(Account, user=self.request.user, pk=pk)
        account.balance = account.calculate()
        serializer = AccountSerializers(account)
        return Response(serializer.data)    

    def put(self, request, pk, format=None):
        if pk != request.data["id"]:
            raise Http404
        account = get_object_or_404(Account, user=self.request.user, pk=pk)
        serializer = AccountSerializers(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        account = get_object_or_404(Account, user=self.request.user, pk=pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PMListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        pms = Payment_Method.objects.filter(user=self.request.user)
        for pm in pms:
            pm.balance = pm.calculate()
        serializer = PMSerializers(pms, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = self.request.data.copy()
        data['user'] = self.request.user.pk
        serializer = PMSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PMDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, pk, format=None):
        pm = get_object_or_404(Payment_Method, user=self.request.user, pk=pk)
        pm.balance = pm.calculate()
        serializer = PMSerializers(pm)
        return Response(serializer.data)    

    def put(self, request, pk, format=None):
        if pk != request.data["id"]:
            raise Http404
        pm = get_object_or_404(Payment_Method, user=self.request.user, pk=pk)
        serializer = PMSerializers(pm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pm = get_object_or_404(Payment_Method, user=self.request.user, pk=pk)
        pm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ExpenseListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        expenses = Expense.objects.filter(user=self.request.user)
        serializer = ExpenseSerializers(expenses, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = self.request.data.copy()
        data['user'] = self.request.user.pk
        serializer = ExpenseSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, pk, format=None):
        expense = get_object_or_404(Expense, user=self.request.user, pk=pk)
        serializer = ExpenseSerializers(expense)
        return Response(serializer.data)    

    def put(self, request, pk, format=None):
        if pk != request.data["id"]:
            raise Http404
        expense = get_object_or_404(Expense, user=self.request.user, pk=pk)
        serializer = ExpenseSerializers(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        expense = get_object_or_404(Expense, user=self.request.user, pk=pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class IncomeListAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        incomes = Income.objects.filter(user=self.request.user)
        serializer = IncomeSerializers(incomes, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = self.request.data.copy()
        data['user'] = self.request.user.pk
        serializer = IncomeSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IncomeDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, pk, format=None):
        income = get_object_or_404(Income, user=self.request.user, pk=pk)
        serializer = IncomeSerializers(income)
        return Response(serializer.data)    

    def put(self, request, pk, format=None):
        if pk != request.data["id"]:
            raise Http404
        income = get_object_or_404(Income, user=self.request.user, pk=pk)
        serializer = IncomeSerializers(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        income = get_object_or_404(Income, user=self.request.user, pk=pk)
        income.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)