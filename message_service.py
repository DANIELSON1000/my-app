# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:06:13 2025

@author: ELINA
"""

# message_service.py
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

TW_SID = os.getenv("TWILIO_ACCOUNT_SID")
TW_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TW_FROM = os.getenv("TWILIO_FROM")

def send_email(to_email, subject, body):
    if not SMTP_USER or not SMTP_PASS:
        return False, "SMTP credentials not set in .env"
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg.set_content(body)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
        return True, "Email yoherejwe"
    except Exception as e:
        return False, str(e)

def send_sms(to_number, body):
    if not (TW_SID and TW_TOKEN and TW_FROM):
        return False, "Twilio credentials not set in .env"
    try:
        client = Client(TW_SID, TW_TOKEN)
        message = client.messages.create(body=body, from_=TW_FROM, to=to_number)
        return True, message.sid
    except Exception as e:
        return False, str(e)
