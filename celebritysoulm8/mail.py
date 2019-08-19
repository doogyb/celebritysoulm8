import smtplib
import traceback


def send_email(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        raise


def send_crash_email(e, chunk):
    with open("keys/mail.txt") as f:
        password = f.read().strip()

    email_contents = ("CHUNK: " + str(chunk) + "\n\n\n")
    email_contents += traceback.format_exc()
    send_email("notifier.samuel.doogan@gmail.com", password,
               "samueldoogan@gmail.com", "celebritysoulm8 crash",
               email_contents)