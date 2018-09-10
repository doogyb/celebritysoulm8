from twitter import *
import time
import os
import pprint


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
        print(("%02d:%02d" % (m, s)))
        time.sleep(1)


def get_url_image_of_user(handle):

    twitter = Twitter(auth=auth_twitter())
    user = twitter.users.lookup(screen_name=handle)
    #pprint.pprint(user)

    return str(user[0]['profile_image_url'])[:-11] + str(user[0]['profile_image_url'])[-4:]


def delete_all_tweets():

    twitter = Twitter(auth=auth_twitter())
    timeline = twitter.statuses.home_timeline()
    print((len(timeline)))

    for tweet in timeline:
        print((tweet['id']))
        print(("Destroying: ", tweet['text']))
        twitter.statuses.destroy(id=tweet['id'])


def auth_twitter():

    consumer_key = open("../keys/consumer-key.txt").read().strip()
    consumer_secret = open("../keys/consumer-secret.txt").read().strip()
    access_token = open("../keys/access-token.txt").read().strip()
    access_token_secret = open("../keys/access-token-secret.txt").read().strip()

    return OAuth(access_token, access_token_secret, consumer_key, consumer_secret)


if __name__ == "__main__":
    #  delete_all_tweets()
    pass
