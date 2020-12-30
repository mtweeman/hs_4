# Standard libraries
import smtplib

# Imported libraries

# My libraries


class Mail:
    """A class for e-mail handling"""
    def __init__(self):
        # Sender account
        self.gmail_user = 'hajlesilesiabrewery@gmail.com'
        self.gmail_password = 'CoMmOnRaIl792'

        # Sender and recipient accounts
        self.mail_from = self.gmail_user
        self.mail_to = 'mtweeman@gmail.com'

        # E-mail
        self.mail_subject = ''
        self.mail_message_body = ''

    def send_mail(self):
        # Prepare e-mail message
        self.mail_message = '''\
From: %s
To: %s
Subject: %s
''' % (self.mail_from, self.mail_to, self.mail_subject)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self.gmail_user, self.gmail_password)
        server.sendmail(self.mail_from, self.mail_to, self.mail_message)
        server.close()

    def battery_notification(self, ispindel_name, battery_min_voltage):
        self.mail_subject = 'Battery needs charging for ' + ispindel_name + ': U <= ' + str(battery_min_voltage)
        self.mail_message_body = ''

        self.send_mail()
