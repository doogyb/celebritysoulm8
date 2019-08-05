from celebritysoulm8 import twitterbot
from celebritysoulm8.mail import send_crash_email
from requests.exceptions import ChunkedEncodingError

chunk = 0

try:
    twitterbot.listen()

except ChunkedEncodingError as e:
    chunk += 1
    send_crash_email(e)
    if chunk == 3:
        raise

except Exception as e:
    send_crash_email(e)
    raise
