from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
import uuid


#Custom ID generator function
def generate_custom_id(prefix, model_class, field_name):
    last_entry = model_class.objects.order_by('-' + field_name).first()
    if last_entry:
        #Extract the numeric part from the last ID and convert it from hex to int
        last_id = last_entry.pk.split('-')[1]
        new_id_int = int(last_id, 16) + 1
    else: 
        new_id_int = 1

    #ensure the new ID does not exceed FFFF
    if new_id_int > 0xFFFF:
        raise ValidationError(f"Maximum ID limit reached.")
    #format the new ID with prefix and hex number added to 4 digits
    return f"{prefix}-{new_id_int:04X}"


#Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)        

        return self.create_user(email, password, **extra_fields)


#user table - the shop owners
class User(AbstractBaseUser, PermissionsMixin):
    userID = models.CharField(max_length=7, primary_key=True, editable=False)
    Fname = models.CharField(max_length=20)
    Lname = models.CharField(max_length=20)
    nationalID = models.CharField(max_length=20, unique=True)
    DoB = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    phoneNo = models.CharField(max_length=15, unique=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Fname', 'Lname', 'nationalID', 'DoB', 'gender', 'phoneNo']

    def save(self, *args, **kwargs):
        if not self.userID: 
            # Generate a new userID using the custom ID generator function
            self.userID = generate_custom_id("US", User, 'userID')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    

class Shop(models.Model):
    shopID = models.CharField(max_length=6, primary_key=True, editable=False)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    shopName = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    industry = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.shopID: 
            # Generate a new shopID using the custom ID generator function
            self.shopID = generate_custom_id("S", Shop, 'shopID')
        super().save(*args, **kwargs)

#stock table - the products in the shop
class Stock(models.Model):
    productID = models.CharField(max_length=6, primary_key=True, editable=False)
    shopID = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(default="NULL") 
    manufacturer = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        #Auto generate productID if not already set
        if not self.productID:
            self.productID = generate_custom_id("P", Stock, 'productID')
        super().save(*args, **kwargs)


#Employee table - the shop employees
class Employee(models.Model):
    employeeID = models.CharField(max_length=6, primary_key=True, editable=False)
    shopID = models.ForeignKey(Shop, on_delete=models.CASCADE)
    Fname = models.CharField(max_length=20)
    Lname = models.CharField(max_length=20)
    nationalID = models.CharField(max_length=20, unique=True)
    DoB = models.DateField()
    gender = models.CharField(max_length=10)
    

    def save(self, *args, **kwargs):
        # Generate a new employeeID using the custom ID generator function
        if not self.employeeID:             
            self.employeeID = generate_custom_id("E", Employee, 'employeeID')
        super().save(*args, **kwargs)



