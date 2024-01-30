from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import views

urlpatterns = [
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/category/', views.CategoryListAPI.as_view(), name = 'categorylist_api'),
    path('api/category/<int:pk>/', views.CategoryDetailAPI.as_view(), name = 'categorydetail_api'),
    path('api/account/', views.AccountListAPI.as_view(), name = 'accountlist_api'),
    path('api/account/<int:pk>/', views.AccountDetailAPI.as_view(), name = 'accountdetail_api'),
    path('api/pm/', views.PMListAPI.as_view(), name = 'pmlist_api'),
    path('api/pm/<int:pk>/', views.PMDetailAPI.as_view(), name = 'pmdetail_api'),
    path('api/expense/', views.ExpenseListAPI.as_view(), name = 'expenselist_api'),
    path('api/expense/<int:pk>/', views.ExpenseDetailAPI.as_view(), name = 'expensedetail_api'),
    path('api/income/', views.IncomeListAPI.as_view(), name = 'incomelist_api'),
    path('api/income/<int:pk>/', views.IncomeDetailAPI.as_view(), name = 'incomedetail_api'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
