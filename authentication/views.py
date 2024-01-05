from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login, authenticate,logout
from django.db.models import Q
from utils import generate_and_send_otp,verify_otp
from django.contrib.auth.hashers import make_password
import os
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.cache import never_cache
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
load_dotenv()


client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])

twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

@never_cache
@login_required(login_url='signin')
def forgetpassword(request, user=0):
    if request.method == 'POST':
        # email_or_phone= request.POST.get('email_or_phone')
        phone = "+91" + request.POST.get('email_or_phone')
        # phone = request.POST.get('email_or_phone')
        phone1 = "+91" + request.POST.get('email_or_phone')
        print(phone1,"phooooooooooookdfjs")

        try:
            user = CustomUser.objects.get(phone = phone1)
            print(user,"userrrrrrrrrrrrrrrr")
        except:            
            messages.error(request,'User not found. Please enter a valid email or ph')




        # print(user,"User....")

        if user:
            if phone:
                print(phone,"oooooooo5555555555555555555555555555555")
                set = send(phone)
                print(set,"oooooooooooooooooooooooooooooo")
                context = {
                    'phone':phone
                }

                return render(request, 'authentication/otp_verification.html', context) 

        else:
            messages.error(request,'User not found. Please enter a valid email or ph')
    return render(request,'authentication/forgetpassword.html')

@never_cache
@login_required(login_url='signin')
def otp_verification(request,phone):
    print(phone,"eeephoneeeeeeeeeeeeeeeee")
    if request.method == 'POST':
       entered_otp = request.POST.get('otp')

       if check(phone, entered_otp):
        
            # change_password_url = reverse('change_password', args=[phone])
            # return redirect(change_password_url)
           return redirect('change_password', phone = phone)
       else:
           return redirect(forgetpassword)

    return render(request, 'authentication/otp_verification.html') 

@never_cache
@login_required(login_url='signin')
def send(phone):
    verify.verifications.create(to=phone, channel='sms')
    print(phone,"phhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

@never_cache
@login_required(login_url='signin')
def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
        print("settttttt")
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'


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
                    # messages.success(request, 'You have successfully signed in as admin.')
                    print(user.is_superuser)
                    print("its a super user.....")
                    # return render(request,'adminpanel/dashboard.html')
                    return redirect('dashboard')
                    
                else:
                    # messages.success(request, 'You have successfully signed in.')
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
        phone_number = "+91" + request.POST['phone_number']
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
        
        #checking if email already exists and if yes redirecting to signup
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Email is already registered. Please login with a different email")
            return redirect('signup')
        
        #checking if phone already exists and if yes redirecting to singup
        if CustomUser.objects.filter(phone=phone_number).exists():
            messages.error(request,"Phone Number is already registered with a different user. Please try with another number")
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

@never_cache
@login_required(login_url='signin')
def change_password(request,phone):
    print(phone,"change Password.....of")
    user = CustomUser.objects.get(phone = phone)
    if request.method =='POST':
        new_password = request.POST.get('new_password')
        repeat_new_password= request.POST.get('repeat_new_password')

        if new_password != repeat_new_password:
            messages.error(request,'Repeat password do not match.Please reenter')
            return redirect('change_password',phone =phone)
        
        if len(new_password) < 6:
            messages.error(request,'Password is too short. It should be atleast 6 characters long')
            return redirect('change_password',phone=phone)
        
        if not any(char.isdigit() for char in new_password):
            messages.error(request,'Password should contain atleast one digit')
            return redirect('change_password',phone=phone)
        
        if not any(char.isalpha() for char in new_password):
            messages.error(request,'Password should contain atleast one letter')
            return redirect('change_password',phone=phone)
        
        
        user.set_password(new_password)
        print(new_password, "NEWWWWW")
        # hashed_password = make_password(new_password) 
        # print(hashed_password,"NEW PASSWORddddd")
        # user.password = hashed_password
        user.save()

        messages.success(request,'Password changed successfully')
        return redirect('signin')
            
    return render(request,'authentication/change_password.html',{'phone':phone})

@never_cache
def home(request):
    return render(request,'home/index.html')

@never_cache
@login_required
def user_logout(request):
    logout(request)
    # messages.success(request, 'Logout successful.')
    return render(request,'home/index.html')

    
