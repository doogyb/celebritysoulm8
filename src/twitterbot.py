import pprint
from datetime import datetime
from twitter import *

import analyse_words
import cross_comparison
from twitter_util import auth_twitter, get_url_image_of_user
import urllib, os.path
import json


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

    with open('../db/twitter/user_queries.json') as f:
        user_queries = json.load(f)

    if [handle, user_match] in user_queries:
        print "User has already matched"
        return
    else:
        with open('../db/twitter/user_queries.json', 'w') as f:
            user_queries.append((handle, user_match))
            json.dump(user_queries, f, indent=4)

    reply_content = "testing @" + handle + " you have matched with: " + user_match

    if not os.path.isfile("../img/" + user_match[1:] + ".jpg"):
        urllib.urlretrieve(get_url_image_of_user(user_match[1:]), "../img/" + user_match[1:] + ".jpg")

    profile_img = "../img/" + user_match[1:] + ".jpg"

    try:

        # Uploading images requires special domain
        t_upload = Twitter(domain='upload.twitter.com', auth=auth_twitter())
        media_id = t_upload.media.upload(media=open(profile_img, 'rb').read())["media_id_string"]
        twitter.statuses.update(status=reply_content, in_reply_to_status_id=status_id, media_ids=media_id)

        log_text = "\n\n----------------------------------------------------\n\n"
        log_text += str(datetime.now()) + "\n\n"
        log_text += "\n\n" + handle + " tried to reply with text: " "\n\n"
        log_text += msg['text']
        log_text += "\n\nReply given was: " + reply_content
        log_text += "\nImage uploaded: " + profile_img
        log_text += "\n\n----------------------------------------------------\n\n"

        pprint.pprint(msg)

        with open("../log/log.txt", 'a') as logfile:
            logfile.write("\n\n" + log_text)

    except TwitterHTTPError as twitter_error:

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


