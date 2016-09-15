from twitter import *
import pprint
import analyse_words


def auth_twitter():

    consumer_key = open("../keys/consumer-key.txt").read().strip()
    consumer_secret = open("../keys/consumer-secret.txt").read().strip()
    access_token = open("../keys/access-token.txt").read().strip()
    access_token_secret = open("../keys/access-token-secret.txt").read().strip()

    return OAuth(access_token, access_token_secret, consumer_key, consumer_secret)


def listen():

    twitter_userstream = TwitterStream(auth=auth_twitter(), domain='userstream.twitter.com')
    for msg in twitter_userstream.user():
            if 'entities' in msg:
                pprint.pprint(msg)
                print msg['entities']['hashtags']
                print msg['in_reply_to_screen_name']
                print

                print 'matchme' in [hashtag['text'].lower() for hashtag in msg['entities']['hashtags']]


def reply(handle, status_id):

    twitter = Twitter(auth=auth_twitter())
    user_score = analyse_words.query(handle)

    reply_content=""
    try:
        twitter.statuses.update(status=reply_content, in_reply_to_status_id=status_id)

    except TwitterHTTPError as twitter_error:

        err_str = "Could not send reply: ", reply_content
        err_str += str(twitter_error)

        # TODO log the err_str

