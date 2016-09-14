from twitter import *
import pprint


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

                print 'matchme' in [hashtag['text'] for hashtag in msg['entities']['hashtags']]

