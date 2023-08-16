#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : email.py
Description      : 
Time             : 2023/08/11 10:49:43
Author           : AllenLuo
Version          : 1.0
'''

from django.core.mail import send_mail


def send_email(request):
    subject = 'Hello'
    message = 'Hi, this is a test email.'
    from_email = 'your_email@example.com'
    recipient_list = ['recipient1@example.com', 'recipient2@example.com']
    send_mail(subject, message, from_email, recipient_list)