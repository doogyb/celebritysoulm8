from twitter import *
import pprint
import analyse_words
import cross_comparison


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

                if msg['in_reply_to_screen_name'] == 'celebritysoulm8' and 'matchme' in [hashtag['text'].lower() for hashtag in msg['entities']['hashtags']]:

                    reply_with_celeb_match(msg)


def reply_with_celeb_match(msg):

    handle = msg['user']['screen_name']
    status_id = msg['id']
    twitter = Twitter(auth=auth_twitter())
    user_score = analyse_words.query(handle)
    user_match = cross_comparison.find_most_similar(user_score)

    reply_content = "@" + handle + " you have matched with: " + user_match

    try:
        twitter.statuses.update(status=reply_content, in_reply_to_status_id=status_id)

        log_text = "----------------------------------------------------"
        log_text += "\n\n" + handle + " tried to reply with text: " "\n\n"
        log_text += msg['text']
        log_text += "\n\nReply given was: " + reply_content
        log_text += "----------------------------------------------------"

        with open("../log/log.txt", 'a') as logfile:
            logfile.write("\n\n" + log_text)

    except TwitterHTTPError as twitter_error:

        err_str = "----------------------------------------------------"
        err_str += "Could not send reply: ", reply_content
        err_str += str(twitter_error)
        err_str += "----------------------------------------------------"

        with open("../log/log.txt", 'a') as logfile:
            logfile.write("\n\n" + err_str)

listen()

