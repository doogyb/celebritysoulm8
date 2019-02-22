import pprint
from datetime import datetime
from twitter import *

from . import analyse_words
from . import cross_comparison
from .twitter_util import auth_twitter, get_url_image_of_user
import urllib.request
import urllib.parse
import urllib.error
import os.path
import json
from . import similarity_measure
import twitter
from pprint import pprint


def listen():

    # twitter_userstream = TwitterStream(auth=auth_twitter(), domain='stream.twitter.com')
    t = twitter.Api(*auth_twitter())
    for msg in t.GetStreamFilter(follow=["773917260050272258"]):

            if 'entities' in msg:
                pprint(msg)
                print(msg['entities'])

                if (msg['in_reply_to_screen_name'] == 'celebritysoulm8' and
                   'matchme' in [hashtag['text'].lower() for hashtag in msg['entities']['hashtags']]):

                    reply_with_celeb_match(msg)

                elif msg['in_reply_to_screen_name'] == 'celebritysoulm8' and \
                     'rateus' in [hashtag['text'].lower() for hashtag in msg['entities']['hashtags']] and \
                     len(msg['entities']['user_mentions']) == 2:

                    reply_with_user_rating(msg)

                else:
                    print("Not for us")
                    # print("Tried but did not work for some reason:\n\n\n ")
                    # print("Message: " + msg['text'] + "\n\n\n")
                    # print(pprint.pprint(msg))

            else:
                # print "Tried but did not work for some reason:\n\n\n "
                # print "Message: " + msg['text'] + "\n\n\n"
                print(pprint.pprint(msg))


def reply_with_celeb_match(msg):

    handle = msg['user']['screen_name']
    status_id = msg['id']
    user_score = analyse_words.query(handle)
    user_match = cross_comparison.find_most_similar(user_score)

    # with open('db/twitter/user_queries.json') as f:
    #     user_queries = json.load(f)
    #
    # if [handle, user_match] in user_queries:
    #     print("User has already matched")
    #     return
    # else:
    #     with open('db/twitter/user_queries.json', 'w') as f:
    #         user_queries.append((handle, user_match))
    #         json.dump(user_queries, f, indent=4)

    reply_content = "@" + handle + " you have matched with: " + user_match
    profile_img = download_user_image(user_match[1:])
    t = twitter.Api(*auth_twitter())
    t.PostUpdate(reply_content, media=open(profile_img, 'rb'))


def reply_with_user_rating(msg):

    status_id = msg['id']
    handle = msg['user']['screen_name']
    other_handle = ""
    for h in msg['entities']['user_mentions']:
        if h['screen_name'] != 'celebritysoulm8':
            other_handle = h['screen_name']

    handle_score = analyse_words.query(handle)
    other_handle_score = analyse_words.query(other_handle)

    similarity = similarity_measure.difference(handle_score, other_handle_score)

    # converting to range of 0 to 100

    similarity = (similarity + 1) * 50

    reply_content = "@" + handle + " you are " + str(int(similarity)) + "/100 alike to @" + other_handle

    try:
        twitter = Twitter(auth=auth_twitter())
        twitter.statuses.update(status=reply_content, in_reply_to_status_id=status_id)
        log(msg, reply_content)

    except TwitterHTTPError as twitter_error:
        log_err(twitter_error, reply_content)


def download_user_image(handle):

    if not os.path.isfile("img/" + handle + ".jpg"):
        urllib.request.urlretrieve(get_url_image_of_user(handle), "img/" + handle + ".jpg")

    profile_img = "img/" + handle + ".jpg"
    return profile_img


def log(msg, reply_content, profile_img=None):

    try:
        handle = msg['user']['screen_name']
        log_text = "\n\n----------------------------------------------------\n\n"
        log_text += str(datetime.now()) + "\n\n"
        log_text += "\n\n" + handle + " tried to reply with text: " "\n\n"
        log_text += msg['text']
        log_text += "\n\nReply given was: " + str(reply_content)
        if profile_img:
            log_text += "\nImage uploaded: " + profile_img
        log_text += "\n\n----------------------------------------------------\n\n"

        pprint.pprint(msg)

        with open("log/log.txt", 'a') as logfile:
            logfile.write("\n\n" + log_text)
    except TypeError as err:
        print(err)
        print("Can't do it captain!")


def log_err(twitter_error, reply_content):

    print(twitter_error)
    err_str = "----------------------------------------------------\n\n"
    err_str += str(datetime.now()) + "\n\n"
    err_str += "Could not send reply: ", str(reply_content)
    err_str += str(twitter_error)
    err_str += "----------------------------------------------------\n\n"

    with open("log/log.txt", 'a') as logfile:
        logfile.write("\n\n" + err_str)


if __name__ == "__main__":
    listen()
