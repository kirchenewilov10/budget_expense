# ***********************************************************************************
# File Name: email.py
# Author: Kane.H
# Created: 2019-11-05
# Description: email module for global usage
# -----------------------------------------------------------------------------------

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ***********************************************************************************
# @Function: Send Email
# @Returns: Status Code
# -----------------------------------------------------------------------------------
def sendEmail(src_email, src_pwd, dest_email, subject, content, smtp_server_domain, smtp_server_port):
    try:
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = 'MovetheBrain'
        message['To'] = dest_email
        part = MIMEText(content, 'html')
        message.attach(part)

        s = smtplib.SMTP(host=smtp_server_domain, port=smtp_server_port)
        s.ehlo()
        s.starttls()
        s.login(src_email, src_pwd)
        s.sendmail(src_email, dest_email, message.as_string())
        s.close()
        return True

    except Exception as e:
        return False
