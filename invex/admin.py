from django.contrib import admin
from .models import User, Shop, Stock, Employee

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userID', 'Fname', 'Lname', 'email', 'phoneNo', 'nationalID')
    search_fields = ('email', 'nationalID')
    ordering = ('userID',)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shopID', 'userID', 'shopName', 'type', 'industry', 'location')
    
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('productID', 'shopID', 'name', 'manufacturer', 'price', 'quantity')
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employeeID', 'Fname', 'Lname', 'nationalID', 'shopID')


