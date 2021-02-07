import os
import imghdr
from email.message import EmailMessage
import smtplib

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

msg = EmailMessage()
msg['Subject'] = 'Grab dinner this weekend?'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS
msg['To'] = ', '.join(contacts)
msg.set_content('Image attached...)

with open('bronx_1.jpg', 'rb') as f:
    file_data = f.read()
    file_type = imghdr.what(f.name)
    file_name = f.name
    # print(file_type)

# files = ['bronx_1.jpg', 'bronx_2.jpg']
# for file in files:
#     with open(file, 'rb') as f:
#         file_data = f.read()
#         file_type = imghdr.what(f.name)
#         file_name = f.name
#
#     msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name )


msg.set_content('How about dinner at 6 pm this Saturday?')
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)


with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    print(EMAIL_ADDRESS)
    print(EMAIL_PASSWORD)
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    subject = 'Grab dinner this weekend?'
    body = 'How about dinner at 7pm this Saturday?'

    msg = f'Subject: {subject}\n\n{body}'
    smtp.sendmail(EMAIL_ADDRESS, 'danielAhodczak@gmail.com', msg)
