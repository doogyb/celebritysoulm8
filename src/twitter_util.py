from twitterbot import auth_twitter
from twitter import *
import time
import os


def wait_time(call):
    twitter = Twitter(auth=auth_twitter())

    rate_status = twitter.application.rate_limit_status(resources=call.split("/")[0])
    reset_time = rate_status['resources'][call.split("/")[0]]['/'+call]
    return int(reset_time['reset'])


def block_until_reset(call):

    reset = wait_time(call)
    while reset - time.time() > 0:

        m, s = divmod(reset - time.time(), 60)
        os.system('clear')
        print "%02d:%02d" % (m, s)
        time.sleep(1)



