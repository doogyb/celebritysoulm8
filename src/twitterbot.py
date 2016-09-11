from twitter import *

consumer_key = open("../keys/consumer-key.txt").read().strip()
consumer_secret = open("../keys/consumer-secret.txt").read().strip()
access_token = open("../keys/access-token.txt").read().strip()
access_token_secret = open("../keys/access-token-secret.txt").read().strip()

t = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

t.statuses.update(status="Testing first status")