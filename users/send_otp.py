from twilio.rest import Client
import os

from dotenv import load_dotenv
load_dotenv()


def send_otp():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    message = client.messages.create(
        body="This is your required otp for login.", from_=TWILIO_PHONE_NUMBER, to='+9779861873263')


# send_otp()
