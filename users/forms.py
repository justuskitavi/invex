from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from invex.models import User, Shop, Stock, Employee
from django.contrib.auth.password_validation import validate_password


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say')
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    DoB = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = User
        fields = ['Fname', 'Lname', 'nationalID', 'DoB', 'gender', 'email', 'phoneNo'] 

        labels = {
            'Fname': 'First Name',
            'Lname': 'Last Name',
            'nationalID': 'National Identification Number',
            'DoB': 'Date of Birth',
            'gender': 'Gender',
            'email': 'email',
            'phoneNo': 'Phone Number',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_phoneNo(self):
        phoneNo = self.cleaned_data['phoneNo']
        if User.objects.filter(phoneNo=phoneNo).exists():
            raise forms.ValidationError("Phone number already exists")
        return phoneNo
    
    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password1')
        pw2 = cleaned_data.get('password2')

        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    def save(self, commit = False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user
    

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label="Enter OTP")
 
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['shopName', 'type', 'industry', 'location']
        labels = {
            'shopName' : 'Name of the Shop',
            'type' : 'Type of the Shop',
            'industry' : 'Industry',
            'location' : 'Location of the Shop',
        }
        widgets = {
            'type' : forms.Select(choices=[('General', 'General'), ('Specialized', 'Specialized')])
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'description', 'manufacturer', 'price', 'quantity', 'threshold']
        labels = {
            'name' : 'Name of the Product',
            'description' : 'Description',
            'manufacturer' : 'Manufacturer',
            'price' : 'Price of the Product',
            'quantity' : 'Quantity',
            'threshold' : 'Threshold',
        }
        widgets = {
            'description' : forms.Textarea(attrs={'rows' : 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['threshold'].initial = 5

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['Fname', 'Lname', 'nationalID', 'DoB', 'gender']

        labels = {
            'Fname': 'First Name',
            'Lname': 'Last Name',
            'nationalID': 'National ID',
            'DoB': 'Date of Birth',
            'gender': 'Gender',
        }
        widgets = {
            'DoB': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),            
        }


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()


class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password1')
        pw2 = cleaned_data.get('password2')

        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords do not match")
        
        validate_password(pw1)
        return cleaned_data


class PasswordConfirmationForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)


class OTPForm(forms.Form):
    otp = forms.CharField(label="Enter OTP", max_length=6, required=True)

class NewPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('new_password1')
        pw2 = cleaned_data.get('new_password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords do not match")
        
        validate_password(pw1)
        return cleaned_data
    

class ProductEditForm(ProductForm):
    class Meta(ProductForm.Meta):
        # Reuse labels/widgets from ProductForm
        exclude = ['quantity']  # Exclude quantity, not editable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

