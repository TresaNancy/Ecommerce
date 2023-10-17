# utils.py
import random
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail

def generate_and_send_otp(destination, is_email=False):
    # Generate a random 6-digit OTP
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    if is_email:
        # Send OTP via email
        subject = 'Your OTP'
        message = f'Your OTP is: {otp}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [destination]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    else:
        # Send OTP via SMS
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            body=f'Your OTP is: {otp}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=destination
        )

    return otp


def verify_otp(entered_otp, generated_otp):
    return entered_otp == generated_otp

