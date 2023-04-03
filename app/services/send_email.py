from flask import render_template, current_app
import boto3
from botocore.exceptions import ClientError
# import requests
# from flask_mail import Message
# from .. import mail
# from app.models import User

class InvalidRegistration(Exception):
    #StandardError
    pass
class EmailProviderError(Exception):
    #StandardError
    pass

class Email:
    def __init__(self, setting):
        self.setting = setting
        self.sender = current_app.config['MAIL_SENDER']
        self.aws_region_ses = current_app.config['AWS_REGION_SES']
        # The character encoding for the email.
        self.charset = "UTF-8"
        # self.mail_url = current_app.config['MAIL_API_URL']
        # self.from_email = current_app.config['MAIL_SENDER']
        # self.mail_api_key = current_app.config['MAIL_API_KEY']
        self.html_email = render_template('auth/email/confirm' + '.html', username = self.setting["username"], 
                                            register_url = self.setting["verification_url"])

    def mail_body_html(self):
        body_html = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
            """
        return body_html

    def mail_body_text(self):
        body_text = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
        return body_text

    def mail_subject(self):
        subject = "Amazon SES Test (SDK for Python)"
        return subject

    def send_email_verification(self):
        # Create a new SES resource and specify a region.
        client = boto3.client('ses',
            region_name=self.aws_region_ses,
            aws_access_key_id = current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key= current_app.config['AWS_SECRET_ACCESS_KEY']
            )

        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        self.setting["email"],
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.charset,
                            'Data': self.mail_body_html(),
                        },
                        'Text': {
                            'Charset': self.charset,
                            'Data': self.mail_body_text(),
                        },
                    },
                    'Subject': {
                        'Charset': self.charset,
                        'Data': self.mail_subject(),
                    },
                },
                Source = self.sender,
                # If you are not using a configuration set, comment or delete the
                # following line
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    """ def mail_json(self):
        msg = {
            "personalizations": [
                {
                "to": [{ 'email': self.setting["email"] }]
            }],
            "from": { 'email': self.from_email },
            "subject": '帳號註冊驗證信｜Bubble',
            "content": [
                { "type": 'text/html',
                "value": self.html_email }
            ]
        }
        return msg

    def send_email_verification(self):
        hed = {'Authorization': f'Bearer {self.mail_api_key}'}
        response = requests.post(self.mail_url, json=self.mail_json(), headers=hed)
        if response.status_code >= 300:
            raise EmailProviderError """

"""     @classmethod
    def send(to, subject, template, **kwargs):
        msg = Message(subject, sender=current_app.config['MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg) """