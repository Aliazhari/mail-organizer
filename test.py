import os
import smtplib

# import logging


EMAIL_ADDRESS = os.environ.get('GMAIL_USER')
EMAIL_PASSWORD = os.environ.get('GMAIL_PASS')
os.environ['TEST_IT'] = 'Hola'

print(EMAIL_ADDRESS, EMAIL_PASSWORD)

# logging.basicConfig(filename='PATH_TO_DESIRED_LOG_FILE',
#                     level=logging.INFO,
#                     format='%(asctime)s:%(levelname)s:%(message)s')


def notify_user():
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'YOUR SITE IS DOWN!'
        body = 'Make sure the server restarted and it is back up'
        msg = f'Subject: {subject}\n\n{body}'

        # logging.info('Sending Email...')
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
        print('done')



notify_user()

