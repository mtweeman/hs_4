# Standard libraries
import httplib2
import os
import base64
from email.mime.text import MIMEText
from apiclient import errors, discovery

# Imported libraries
import oauth2client
from oauth2client import client, tools, file

# My libraries


class Mail:
    """A class for e-mail handling"""
    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/gmail.send'
        self.CLIENT_SECRET_FILE = 'data/credentials.json'
        self.APPLICATION_NAME = 'Gmail API Python Send Email'

        # Sender and recipient accounts
        self.to = 'mtweeman@gmail.com'
        self.sender = 'hajlesilesiabrewery@gmail.com'

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def create_message(self, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = self.to
        message['from'] = self.sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')}

    def send_message(self, message):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)

        try:
            message = (service.users().messages().send(userId='me', body=message).execute())
            return message
        except errors.HttpError:
            pass

    def battery_notification(self, ispindel_name, battery_min_voltage):
        subject = 'Battery needs charging for ' + ispindel_name + ': U <= ' + str(battery_min_voltage) + ' V'
        message_text = ''

        msg = self.create_message(subject, message_text)
        self.send_message(msg)

    def fermentation_start_notification(self, batch_number, batch_name):
        subject = 'Fermentation start of batch ' + str(batch_number) + ', ' + batch_name
        message_text = ''

        msg = self.create_message(subject, message_text)
        self.send_message(msg)
