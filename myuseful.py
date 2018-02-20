import time
import math
import hashlib
import binascii
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import datetime
import socket
import fcntl
import struct

import unicodecsv

GMAIL_USER = u'akuino6002@gmail.com'
GMAIL_PASS = u'My_Password6002'
SMTP_SERVER = u'smtp.gmail.com'
SMTP_PORT = 587
csvDir = "../ELSAcsv/csv/"

datetimeformat = "%Y-%m-%d %H:%M:%S"


def get_timestamp():
    now = time.time()
    now = math.floor(float(now))
    now = int(now)
    return now


def encrypt(password, salt):
    sha = hashlib.pbkdf2_hmac('sha256', password, salt, 126425)
    return binascii.hexlify(sha)


def send_email(recipient, subject, text):
    smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = u'To:' + recipient + u'\n' + u'From: ' + GMAIL_USER
    header = header + '\n' + u'Subject:' + subject + u'\n'

    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['From'] = GMAIL_USER
    msg['To'] = recipient
    msg['Subject'] = Header(
        subject.encode('utf-8'),
        'UTF-8'
    ).encode()

    _attach = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    msg.attach(_attach)

    smtpserver.sendmail(GMAIL_USER, recipient, msg.as_string())
    smtpserver.close()


def timestamp_to_date(now, format=datetimeformat):
    return datetime.datetime.fromtimestamp(int(now)).strftime(format)


def timestamp_to_time(now):
    return str(datetime.timedelta(seconds=now))


def get_time():
    now = int(time.time())
    return datetime.datetime.fromtimestamp(now).strftime(datetimeformat)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def date_to_timestamp(date):
    try:
        tmp = datetime.datetime.strptime(date, datetimeformat)
    except:  # old format ?
        tmp = datetime.datetime.strptime(date, "%H:%M:%S  -  %d/%m/%y")
    return (tmp - datetime.datetime(1970, 1, 1)).total_seconds()


def transform_date(date):
    try:
        tmp = datetime.datetime.strptime(date, datetimeformat).isoformat()
    except:  # old format ?
        tmp = datetime.datetime.strptime(
            date, "%H:%M:%S  -  %d/%m/%y").isoformat()
    return tmp


def now():
    return unicode(datetime.datetime.now().strftime(datetimeformat))
