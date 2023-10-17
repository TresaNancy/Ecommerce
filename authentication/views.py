from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login, authenticate,logout
from django.db.models import Q
from utils import generate_and_send_otp,verify_otp
import os
from twilio.rest import Client
from django.conf import settings
from django.views.decorators.cache import never_cache


# Create your views here.
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Using request.POST.get() to avoid KeyError
        password = request.POST.get('password')

        # print("Email:", email)
        # print("Password:", password)

        try:
            user = authenticate(request, email=email, password=password)
            print(user)

            if user is not None:
                login(request, user)
                print("loged in.........")
                if user.is_superuser:
                    messages.success(request, 'You have successfully signed in as admin.')
                    print(user.is_superuser)
                    print("its a super user.....")
                    # return render(request,'adminpanel/dashboard.html')
                    return redirect('dashboard')
                    
                else:
                    messages.success(request, 'You have successfully signed in.')
                    return redirect('home')  # Redirect to the home page or any other desired page after successful login
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        except Exception as e:
            # Handle authentication exceptions (e.g., AuthenticationFailed)
            messages.error(request, 'An error occurred during authentication.')

    return render(request, 'authentication/signin.html')


def signup(request):
    
    if request.method == 'POST':
        # Get form data from request
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        # Check if passwords match
        if password != repeat_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        if len(password) < 6:
            messages.error(request, 'Password should be at least 6 characters long.')
            return redirect('signup')
        
        if not any(char.isdigit() for char in password):
            messages.error(request, 'Password should contain at least one digit.')
            return redirect('signup')
        
        if not any(char.isalpha() for char in password):
            messages.error(request, 'Password should contain at least one letter.')
            return redirect('signup')

        # Create a new CustomUser object and save it
        try:
            user = CustomUser.objects.create_user(
                email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone_number,
            password=password
        )
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Please sign in.')
            return redirect('signin')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('signup')
    return render(request,'authentication/signup.html')

def forgetpassword(request):
    if request.method == 'POST':
        email_or_phone= request.POST.get('email_or_phone')
        user = CustomUser.objects.filter(Q(email=email_or_phone) | Q(phone=email_or_phone)).first()
        print(user,"User....")
        if user:
            is_email = '@' in email_or_phone
            otp =generate_and_send_otp(email_or_phone,is_email=is_email)
            request.session ['otp'] = otp
            request.session['user_id']=user.id

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            verify_service_sid = settings.TWILIO_VERIFY_SERVICE_SID
            verified_number = settings.TWILIO_PHONE_NUMBER
            
            verification = client.verify.v2.services(verify_service_sid).verifications.create(
                to=verified_number,
                channel="sms"
            )
            
            print(verification.status)  # Check Twilio sta
            return render(request,'otp_verification.html', {'user':user})
        else:
            messages.error(request,'User not found. Please enter a valid email or ph')
    return render(request,'authentication/forgetpassword.html')
   

def otp_verification(request):
    if request.method == 'POST':
       entered_otp = request.post.get('otp')

       if 'otp' in request.session:
            # Get the stored OTP from the session
            stored_otp = request.session['otp']

            # Verify the entered OTP with the stored OTP
            if verify_otp(entered_otp, stored_otp):  # Replace with your OTP verification logic
                # OTP matches, redirect to the change password page
                return redirect('change_password')
            else:
                # OTP doesn't match, display an error message
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
            # OTP not found in the session, handle this case accordingly
            messages.error(request, 'OTP session expired. Please request a new OTP.')

    return render(request, 'authentication/otp_verification.html') 

def change_password(request):
    return render(request,'authentication/change_password.html')

def home(request):
    return render(request,'home/index.html')

@never_cache
def user_logout(request):
    logout(request)
    # messages.success(request, 'Logout successful.')
    return render(request,'home/index.html')

    
