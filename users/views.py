from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, ShopForm, ProductForm, EmployeeForm, OTPVerificationForm, PasswordResetRequestForm, SetNewPasswordForm, PasswordConfirmationForm, NewPasswordForm, OTPForm, ProductEditForm
from django.http import JsonResponse
import json, random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from invex.models import User, Shop, Stock, Employee, Sales
from datetime import date
from django.utils import timezone
from django.db import transaction

def generate_otp():
    return str(random.randint(100000, 999999))


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user_data = form.cleaned_data.copy()
            user_data['DoB'] = user_data['DoB'].isoformat()
            request.session['user_data'] = user_data
            otp = generate_otp()
            request.session['otp'] = otp
            send_mail(
                'Your Invex Email Verification OTP',
                f'Your OTP for invex registration is: {otp}', 
                settings.EMAIL_HOST_USER,
                [form.cleaned_data['email']],
                fail_silently=False
            )  

            messages.info(request, 'An OTP has been sent to your email. Please verify to continue.') 
            return redirect('verify-otp')         
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            session_otp = form.cleaned_data['otp']
            user_data = request.session.get('user_data', {})
            if entered_otp == entered_otp == session_otp and user_data:
                user_data['DoB'] = date.fromisoformat(user_data['DoB'])  
                    
                user = User(
                    Fname=user_data['Fname'],
                    Lname=user_data['Lname'],
                    nationalID=user_data['nationalID'],
                    DoB=user_data['DoB'],
                    gender=user_data['gender'],
                    email=user_data['email'],
                    phoneNo=user_data['phoneNo'],
                    is_active=True
                )
                user.set_password(user_data['password1'])
                user.save()

                request.session.pop('otp', None)
                request.session.pop('user_data', None)

                messages.success(request, 'Account created successfully. Now use your credentialsto log in.')
                return redirect('login')
            
        else:
            messages.error(request, 'Invalid OTP or session expired.')
    else:
        form = OTPVerificationForm()
        return render(request, 'users/verify_otp.html', {'form' : form})


def resend_otp(request):
    user_data = request.session.get('user_data', {})
    
    if user_data:
        otp = generate_otp()
        request.session['otp'] = otp
        send_mail(
            'Your Invex Resent OTP',
            f'Your new OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [user_data['email']],
            fail_silently=False
        )
        return redirect('verify-otp')
    else:
        messages.error(request, 'Session expired. Please register again.')


def loginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email = email, password = password)

        if user is not None: 
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('invex-home')
        else: 
            return render(request, 'users/login.html', {
                'error': 'Either the email or the password is wrong. Please check again.'
            })
    return render(request, 'users/login.html')   

def logoutView(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')        


def forgot_password(request):
    form = PasswordResetRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            request.session['reset_email'] = email
            request.session['reset_otp'] = otp

            send_mail(
                'Invex Password Reset OTP',
                f'Your password reset OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            request.session['otp_time'] = timezone.now().isoformat()
            messages.success(request, 'An OTP has been send to your email.')
            return redirect('verify-reset-otp')
        except User.DoesNotExist:
            messages.error(request, 'No user with this email was found.')

    return render(request, 'users/forgot_password.html', {
        'form' : form, 
        'show_register': True
    })


def verify_reset_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if entered_otp == request.session.get('reset_otp'):
                request.session['reset_otp_verified'] = True
                return redirect('set-new-password')
            else:
                messages.error(request, 'Ivalid OTP')
    else:
        form = OTPVerificationForm()

    return render(request, 'users/verify_reset_otp.html', {'form' : form})


def set_new_password(request):
    if not request.session.get('reset_otp_verified'):
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            email = request.session.get('reset_email')
            try:
                user = User.objects.get(email=email)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                send_mail(
                    subject='Your Invex password was reset',
                    message=(
                        "If this was you, no action is needed. "
                        "If not, please change your password immediately using the link below:\n"
                        "https://yourdomain.com/change-password/"  # You can update this later
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],  # 👈 FIXED
                    fail_silently=False
                )


                for key in ['reset_email', 'reset_otp', 'reset_otp_verified']:
                    request.session.pop(key,None)

                messages.success(request, 'Password reset successfully. You may now login')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Something went wrong. Please try again.')

    else:
        form = SetNewPasswordForm()

    return render(request, 'users/set_new_password.html',{'form' : form})

def resend_otp(request):
    email = request.session.get('reset_email')
    if email:
        try:
            User.objects.get(email=email)
            otp = generate_otp()
            request.session['reset_otp'] = otp
            request.session['otp_time'] = timezone.now().isoformat()

            send_mail(
                'Your new OTP from Invex',
                f'Your new OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            messages.success(request, 'New OTP sent successfully.')
        except User.DoesNotExist:
            messages.error(request, 'No account associated with this email.')
    else:
        messages.success(request, 'Session expired. Start over.')        
        return redirect('forgot-password')
    
    return redirect('verify-reset-otp')

@login_required
def profile(request):
    shops = Shop.objects.filter(userID=request.user)
    employees = Employee.objects.filter(shopID__userID=request.user)

    return render(request, 'users/profile.html', {
        'shops': shops,
        'employees': employees,
    })

@login_required
def create_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit = False)
            shop.userID = request.user
            shop.save()
            return redirect('view-shop')
        
    else:
        form = ShopForm()
    
    return render(request, 'users/create_shop.html', {'form': form})

#View shop - will display the  shops owned.
@login_required
def view_shop(request):
    try:
        shops = Shop.objects.filter(userID=request.user)
        products = Stock.objects.filter(shopID__in=shops)

    except Shop.DoesNotExist:
        shops = None
        products = []

    return render(request, 'users/view_shop.html', {
        'shops': shops,
        'products': products
        })


@login_required
def shop_detail(request, shopID):
    shop = get_object_or_404(Shop, shopID=shopID, userID=request.user)
    products = Stock.objects.filter(shopID=shop)

    return render(request, 'users/shop_detail.html', {
        'shop': shop, 
        'products': products,
        })


@login_required
@csrf_exempt
def add_product(request, shopID):
    shop = get_object_or_404(Shop, shopID=shopID, userID=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.shopID = shop
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('shop-detail', shopID=shop.shopID)
    else:
        form = ProductForm()

    return render(request, 'users/add_product.html', {'form': form, 'shop': shop})


@login_required
@csrf_exempt
def add_stock(request, shopID, productID):
    product = get_object_or_404(Stock, productID=productID, shopID__shopID=shopID)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            password = data.get('password')
            quantity = int(data.get('quantity'))
            
            if not request.user.check_password(password):
                return JsonResponse({'error': 'Incorrect password'}, status=400)            
            
            if quantity < 1:
                return JsonResponse({'error': 'Quantity must be positive number'}, status=400)
            
            product.quantity += quantity
            product.save()
            return JsonResponse({'success': True})
        
        except ValueError:
            return JsonResponse({'error': 'Quantity must be a number'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@csrf_exempt
@transaction.atomic
def sell_product(request, shopID, productID):
    product = get_object_or_404(
        Stock.objects.select_related('shopID'), 
        productID=productID, 
        shopID__shopID=shopID
        )

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity'))

            if quantity < 1:
                return JsonResponse({'error': 'Quantity must be a positive number'}, status=400)
            if quantity > product.quantity:
                return JsonResponse({'error': 'Not enough stock'}, status=400)

            # Decrement stock
            product.quantity -= quantity
            product.save()

            # Create sale record
            Sales.objects.create(
                product=product,
                quantity=quantity,
                total_price=quantity * product.price
            )

            # Send alert if stock is below threshold or out
            subject, message = None, None                 

            if product.quantity == 0:
                subject = 'Product Out of Stock'
                message = f'The product {product.name}, Description: "{product.description}" in shop {product.shopID.shopName} is now out of stock.'
            elif product.quantity <= product.threshold:
                subject = 'Low Stock Warning'
                message = f'The product {product.name}, Description: "{product.description}" in shop {product.shopID.shopName} is low on stock.\nRemaining: {product.quantity} units.'

            if subject and message:              

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False
                )

            return JsonResponse({'success': True})

        except ValueError:
            return JsonResponse({'error': 'Quantity must be a number'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def employee_list(request):
    try: 
        shop = Shop.objects.get(userID=request.user)
        employees = Employee.objects.filter(shopID=shop)

    except Shop.DoesNotExist:
        employees = None

    return render(request, 'users/employees.html', {
        'employees': employees,
    })

@login_required
def add_employee(request):
    try:
        shop = Shop.objects.get(userID=request.user)

    except Shop.DoesNotExist:
        messages.error(request, "You must create a shop first.")
        return redirect('create-shop')
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            emp = form.save(commit=False)
            emp.shopID = shop
            emp.save()
            messages.success(request, "Employee added successfully!")
            return redirect('employee-list')
    else:
        form = EmployeeForm()

    return render(request, 'users/add_employee.html', {'form': form,})


@login_required
def fire_employee(request, employeeID):

    if request.method == 'POST':        
        try: 
            data = json.loads(request.body)
            password = data.get('password')

            if not request.user.check_password(password):
                return JsonResponse({'error': 'Incorrect password'}, status=400)

            emp = get_object_or_404(Employee, employeeID=employeeID)
            emp.delete()
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@login_required
def change_password_request(request):
    if request.method == 'POST':
        form = PasswordConfirmationForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['current_password']):
                otp = generate_otp()
                request.session['change_otp'] = otp
                request.session['change_user_email'] = request.user.email

                send_mail(
                    subject="Your Invex Change Password OTP",
                    message=f"Your OTP is: {otp}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[request.user.email],
                    fail_silently=False
                )
                return redirect('verify-change-otp')
            else:
                messages.error(request, 'Incorrect current password.')

    else:
        form = PasswordConfirmationForm()
    return render(request, 'users/change_password_confirm.html', {'form' : form})

@login_required
def verify_change_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == request.session.get('change_otp'):
                return redirect('set-changed-password')
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = OTPForm()
    return render(request, 'users/verify_change_otp.html', {'form': form})


@login_required
def resend_change_otp(request):
    otp = generate_otp()
    request.session['change_otp'] = otp

    send_mail(
        subject="Your Resent OTP for Password Change",
        message=f"Your new OTP is: {otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.session.get('change_user_email')],
        fail_silently=False
    )
    messages.info(request, "A new OTP has been sent.")
    return redirect('verify-change-otp')


@login_required
def set_changed_password(request):
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password1'])
            user.save()

            send_mail(
                subject="Your password was changed",
                message="Your password has been changed successfully. If this was not you, click here: [LINK]",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False
            )
            messages.success(request, "Password changed. Please login.")
            return redirect('login')
    else:
        form = NewPasswordForm()
    return render(request, 'users/set_changed_password.html', {'form': form})

@login_required
@csrf_exempt
def edit_product(request, shopID, productID):
    product = get_object_or_404(Stock, productID=productID, shopID__shopID=shopID)

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            # This is the password-auth request
            data = json.loads(request.body)
            password = data.get('password')

            user = authenticate(request, email=request.user.email, password=password)
            if not user:
                return JsonResponse({'error': 'Authentication failed'}, status=403)

            form = ProductEditForm(instance=product)
            form_html = render(request, 'users/edit_product.html', {
                'form': form,
                'shopID': shopID,
                'productID': productID
            }).content.decode('utf-8')

            return JsonResponse({'success': True, 'form_html': form_html})
    
        else:
            # This is the actual form submission
            form = ProductEditForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            return JsonResponse({'error': 'Invalid form data'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@csrf_exempt
def delete_product(request, shopID, productID):
    product = get_object_or_404(
        Stock,
        productID=productID,
        shopID__shopID=shopID
    )
    if request.method == 'POST':
        data = json.loads(request.body)
        password = data.get('password')

        user = authenticate(request, email=request.user.email, password=password)
        if not user:
            return JsonResponse({'error': 'Authentication failed'}, status = 403)
        
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status = 403)



@login_required
@csrf_exempt
@require_POST
def delete_shop(request, shopID):
    try:
        data = json.loads(request.body)
        password = data.get('password')

        user = authenticate(request, email=request.user.email, password=password)
        if not user:
            return JsonResponse({'error': 'Authentication failed'}, status=403)

        shop = get_object_or_404(Shop, shopID=shopID, userID=request.user)
        shop.delete()
        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
            