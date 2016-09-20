import pprint
from datetime import datetime
from twitter import *

import analyse_words
import cross_comparison
from twitter_util import auth_twitter, get_url_image_of_user
import urllib, os.path
import json
import similarity_measure


def listen():

    twitter_userstream = TwitterStream(auth=auth_twitter(), domain='userstream.twitter.com')
    for msg in twitter_userstream.user():
            if 'entities' in msg:

                if msg['in_reply_to_screen_name'] == 'celebritysoulm8' and \
                   'matchme' in [hashtag['text'].lower() for hashtag in msg['entities']['hashtags']]:

                    reply_with_celeb_match(msg)

                elif msg['in_reply_to_screen_name'] == 'celebritysoulm8' and \
                     'rateus' in [hashtag['text'].lower() for hashtag in msg['entities']['hashtags']] and \
                     len(msg['entities']['user_mentions']) == 2:

                    reply_with_user_rating(msg)

                else:
                    print pprint.pprint(msg)


def reply_with_celeb_match(msg):

    handle = msg['user']['screen_name']
    status_id = msg['id']
    user_score = analyse_words.query(handle)
    user_match = cross_comparison.find_most_similar(user_score)

    with open('../db/twitter/user_queries.json') as f:
        user_queries = json.load(f)

    if [handle, user_match] in user_queries:
        print "User has already matched"
        return
    else:
        with open('../db/twitter/user_queries.json', 'w') as f:
            user_queries.append((handle, user_match))
            json.dump(user_queries, f, indent=4)

    reply_content = "@" + handle + " you have matched with: " + user_match

    if not os.path.isfile("../img/" + user_match[1:] + ".jpg"):
        urllib.urlretrieve(get_url_image_of_user(user_match[1:]), "../img/" + user_match[1:] + ".jpg")

    profile_img = "../img/" + user_match[1:] + ".jpg"

    try:

        twitter = Twitter(auth=auth_twitter())

        # Uploading images requires special domain
        t_upload = Twitter(domain='upload.twitter.com', auth=auth_twitter())
        media_id = t_upload.media.upload(media=open(profile_img, 'rb').read())["media_id_string"]
        twitter.statuses.update(status=reply_content, in_reply_to_status_id=status_id, media_ids=media_id)

        log(msg, reply_content, profile_img)

    except TwitterHTTPError as twitter_error:
        log_err(twitter_error, reply_content)


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


def log(msg, reply_content, profile_img=None):

    handle = msg['user']['screen_name']
    log_text = "\n\n----------------------------------------------------\n\n"
    log_text += str(datetime.now()) + "\n\n"
    log_text += "\n\n" + handle + " tried to reply with text: " "\n\n"
    log_text += msg['text']
    log_text += "\n\nReply given was: " + reply_content
    if profile_img:
        log_text += "\nImage uploaded: " + profile_img
    log_text += "\n\n----------------------------------------------------\n\n"

    pprint.pprint(msg)

    with open("../log/log.txt", 'a') as logfile:
        logfile.write("\n\n" + log_text)


def log_err(twitter_error, reply_content):

    print twitter_error
    err_str = "----------------------------------------------------\n\n"
    err_str += str(datetime.now()) + "\n\n"
    err_str += "Could not send reply: ", str(reply_content)
    err_str += str(twitter_error)
    err_str += "----------------------------------------------------\n\n"

    with open("../log/log.txt", 'a') as logfile:
        logfile.write("\n\n" + err_str)


if __name__ == "__main__":
    listen()


