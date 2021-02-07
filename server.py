from dataclasses import dataclass
import os
import time
from functools import cached_property, singledispatchmethod
import imghdr
import argparse
from collections import namedtuple
import smtplib
from email.message import EmailMessage
import sqlite3
import client, device

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


@dataclass
class SecurItAlert:
    alert_id: int
    images: list[bytes]
    time: str

    def __init__(self, packet: bytes):
        pass
        """
        TODO: How is the packet encoded by the Arduino,
        and how is it decoded by the server to be processed and
        passed along to SMS or SMTP?
        """


class SecurItServer:
    @classmethod
    def submit_email_basic(cls, alert: SecurItAlert):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            msg = "Subject: Grab dinner this weekend?\n\n" \
                  "How about dinner at 7pm this Saturday?"
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

    @classmethod
    def submit_email(cls, alert: SecurItAlert):
        msg = EmailMessage()
        msg['Subject'] = "SecurIt Alert"
        msg['From'] = EMAIL_ADDRESS

        if args.skip_client:
            msg['To'] = EMAIL_ADDRESS
        else:
            msg['To'] = ', '.join(client.email for client in alert.clients)
        if args.skip_packet:
            msg.set_content(time.asctime())
            with open('meme.jpeg', 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
            # msg.set_content(f"Time is {time.asctime()}")
        else:
            for i, image in enumerate(alert.images):
                msg.add_attachment(image, maintype='image', subtype='jpeg', filename=f'image_{i}.jpeg')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

    def submit_sms(self, alert: SecurItAlert):
        pass


#     TODO: Implement SMS transfer

@dataclass
class Arguments:
    clients: list[Client]
    devices: list[Device]
    skip_client: bool
    skip_packet: bool


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--devices', type=str, help='device database to be (re)built')
    args.add_argument('--skip_client', type=bool, default=False, help="skip the database;"
                                                                      "send with default credentials")
    args.add_argument('--skip_packet', type=bool, default=False, help="skip the packet"
                                                                      "send the default packet")
    args = args.parse_args(namespace=Arguments)

    SecurItServer.submit_email(None)
    # SecurItServer.submit_email_basic(None)
