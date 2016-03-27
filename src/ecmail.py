#!/usr/bin/env python

""" ecmail - EC email library
Tiny support library, allowing e-mails to be send from Python programs, in an easy way.
A typical call looks like this:
ecmail.email_simple("New hot subject", "Long string with body text, usually with many lines", 'someone@domain.net') """

import smtplib
from email.mime.text import MIMEText

__author__ = "Martin Hvidberg"
__email__ = "martin@hvidberg.net"
__repo__ = "https://MartinHvidberg@bitbucket.org/MartinHvidberg/pygewatch"

def email_simple(sub_in="This is the subject string", msg_in="This is the message body ...", to_in="me@home.net"):
    ec_server = 'mail.domain.net'# <--- Your e-mail server ------ Edit this before using -------------
    ec_sender = 'me@domain.net' # <--- Your sender e-mail address ------ Edit this before using -------------
    ec_paswrd = 'my_password' # <--- The password to go with the above ----- Edit this before using -------------
    msg = MIMEText(msg_in)
    msg['Subject'] = sub_in
    msg['From'] = ec_sender
    msg['To'] = to_in
    s = smtplib.SMTP(ec_server, 587)
    s.starttls()
    s.login(ec_sender, ec_paswrd)
    s.sendmail(ec_sender, [to_in], msg.as_string())
    s.quit()