import smtplib
from email.mime.text import MIMEText

def email_simple(sub_in="This is the subject string", msg_in="This is the message body ...", to_in="me@home.net"):
    ec_server = 'mail.domain.net'# <--- Edit this before using -------------
    ec_sender = 'me@domain.net' # <--- Edit this before using -------------
    ec_paswrd = 'my_password' # <--- Edit this before using -------------
    msg = MIMEText(msg_in)
    msg['Subject'] = sub_in
    msg['From'] = ec_sender
    msg['To'] = to_in
    s = smtplib.SMTP(ec_server, 587)
    s.starttls()
    s.login(ec_sender, ec_paswrd)
    s.sendmail(ec_sender, [to_in], msg.as_string())
    s.quit()