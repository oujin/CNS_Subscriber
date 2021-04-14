import smtplib
from email.mime.text import MIMEText
import json


with open("Spider/config_local.json", 'r', encoding='utf8') as f:
    config_local = json.load(f)
    mail_host = config_local["mail_host"]
    mail_user = config_local["mail_user"]
    mail_pass = config_local["mail_pass"]
    sender = config_local["sender"]


def sendmail(receivers, subject, content):
    message = MIMEText(content, 'html', 'GB18030')
    message['From'] = sender
    message['To'] = ','.join(receivers)
    message['Subject'] = subject
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        res = smtpObj.sendmail(sender, receivers, message.as_string())
        print(res)
        print('Successful!')
    except smtplib.SMTPException:
        print('Error!')
