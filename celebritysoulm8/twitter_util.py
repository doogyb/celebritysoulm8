from twitter import Twitter
import time
import os
import twitter


def wait_time(call):
    twitter = Twitter(auth=auth_twitter())

    rate_status = twitter.application.rate_limit_status(
        resources=call.split("/")[0])
    reset_time = rate_status['resources'][call.split("/")[0]]['/' + call]
    return int(reset_time['reset'])


def block_until_reset(call):

    reset = wait_time(call)
    while reset - time.time() > 0:

        m, s = divmod(reset - time.time(), 60)
        os.system('clear')
        print(("%02d:%02d" % (m, s)))
        time.sleep(1)


def get_url_image_of_user(handle):

    t = twitter.Api(*auth_twitter())
    user = t.UsersLookup(screen_name=handle)
    return user[0].profile_image_url.replace("_normal", "")


def delete_all_tweets():

    t = twitter.Api(*auth_twitter())
    timeline = t.GetUserTimeline(screen_name='celebritysoulm8')
    print((len(timeline)))

    for tweet in timeline:

        print("Destroying: ", tweet.text)
        t.DestroyStatus(t.id)


def auth_twitter():

    consumer_key = open("keys/consumer-key.txt").read().strip()
    consumer_secret = open("keys/consumer-secret.txt").read().strip()
    access_token = open("keys/access-token.txt").read().strip()
    access_token_secret = open("keys/access-secret.txt").read().strip()

    return consumer_key, consumer_secret, access_token, access_token_secret


if __name__ == "__main__":
    pass
