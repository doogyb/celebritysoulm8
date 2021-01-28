#! /usr/bin/python3

from celebritysoulm8.twitterbot import TwitterBot
from celebritysoulm8.mail import send_crash_email
from requests.exceptions import ChunkedEncodingError


def main():
    chunking_errors = 0
    twitterbot = TwitterBot()

    print("Celebritysoulm8 now listening...")


    while True:
        try:
            twitterbot.listen()

        except ChunkedEncodingError as e:
            chunking_errors += 1
            twitterbot.log_err(e)

        except Exception as e:
            send_crash_email(e)
            raise
