from celebritysoulm8.twitterbot import TwitterBot
from celebritysoulm8.mail import send_crash_email
from requests.exceptions import ChunkedEncodingError

chunking_errors = 0
twitterbot = TwitterBot()


while True:
    try:
        twitterbot.listen()

    except ChunkedEncodingError as e:
        chunking_errors += 1
        twitterbot.log_err(e)

    except Exception as e:
        send_crash_email(e)
        raise
