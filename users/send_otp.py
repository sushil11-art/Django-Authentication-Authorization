from twilio.rest import Client
import os

from dotenv import load_dotenv
load_dotenv()


def send_otp(otp, mobile):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    body = "This is your required otp for login"+str(otp)
    mobile = mobile
    message = client.messages.create(
        body=body, from_=TWILIO_PHONE_NUMBER, to=mobile)


# send_otp()
