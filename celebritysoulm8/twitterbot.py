from pprint import pprint
from datetime import datetime
from . import analyse_words
from . import cross_comparison
from .twitter_util import auth_twitter, get_url_image_of_user
import urllib.request
import urllib.parse
import urllib.error
import os.path
from . import similarity_measure
import twitter


class TwitterBot:

    def __init__(self):
        self.t = twitter.Api(*auth_twitter())

    def listen(self):

        for msg in self.t.GetStreamFilter(follow=["773917260050272258"]):

            if 'entities' not in msg:
                continue

            pprint(msg)
            print(msg['entities'])

            hashtags = [hashtag['text'].lower()
                        for hashtag in msg['entities']['hashtags']]

            if self.is_reply_with_celeb_match(msg, hashtags):
                self.reply_with_celeb_match(msg)

            elif self.is_reply_with_user_rating(msg, hashtags):
                self.reply_with_user_rating(msg)

    @staticmethod
    def is_reply_with_celeb_match(msg, hashtags):
        return (msg['in_reply_to_screen_name'] == 'celebritysoulm8'
                and 'matchme' in hashtags)

    @staticmethod
    def is_reply_with_user_rating(msg, hashtags):
        return ('rateus' in hashtags
                and len(msg['entities']['user_mentions']) == 2)

    def reply_with_celeb_match(self, msg):

        handle = msg['user']['screen_name']
        user_score = analyse_words.query(handle)
        user_match = cross_comparison.find_most_similar(user_score)

        reply_content = "@" + handle + " you have matched with: " + user_match
        profile_img = self.download_user_image(user_match[1:])

        self.t.PostUpdate(reply_content, media=open(profile_img, 'rb'))

    def reply_with_user_rating(self, msg):

        status_id = msg['id']
        handle = msg['user']['screen_name']
        user_mentions = msg['entities']['user_mentions']
        if user_mentions[0]['screen_name'] != 'celebritysoulm8':
            other_handle = user_mentions[0]['screen_name']
        else:
            other_handle = user_mentions[1]['screen_name']

        handle_score = analyse_words.query(handle)
        other_handle_score = analyse_words.query(other_handle)
        similarity = similarity_measure.difference(
            handle_score, other_handle_score)
        similarity = (similarity + 1) * 50

        reply_content = "@" + handle + " you are " + \
            str(int(similarity)) + "/100 alike to @" + other_handle

        try:
            self.t.PostUpdate(status=reply_content,
                              in_reply_to_status_id=status_id)
            self.log(msg, reply_content)

        except Exception as twitter_error:
            self.log_err(twitter_error, reply_content)

    @staticmethod
    def download_user_image(handle):

        if not os.path.isfile("img/" + handle + ".jpg"):
            urllib.request.urlretrieve(get_url_image_of_user(handle),
                                       "img/" + handle + ".jpg")

        profile_img = "img/" + handle + ".jpg"
        return profile_img

    @staticmethod
    def log(msg, reply_content, profile_img=None):

        try:
            handle = msg['user']['screen_name']
            log_text = "\n\n----------------------------------------------\n\n"
            log_text += str(datetime.now()) + "\n\n"
            log_text += "\n\n" + handle + " tried to reply with text: " "\n\n"
            log_text += msg['text']
            log_text += "\n\nReply given was: " + str(reply_content)
            if profile_img:
                log_text += "\nImage uploaded: " + profile_img
            log_text += "\n\n---------------------------------------------\n\n"

            pprint.pprint(msg)

            with open("log/log.txt", 'a') as logfile:
                logfile.write("\n\n" + log_text)
        except TypeError as err:
            print(err)
            print("Can't do it captain!")

    @staticmethod
    def log_err(twitter_error, reply_content):

        print(twitter_error)
        err_str = "----------------------------------------------------\n\n"
        err_str += str(datetime.now()) + "\n\n"
        err_str += "Could not send reply: " + str(reply_content)
        err_str += str(twitter_error)
        err_str += "----------------------------------------------------\n\n"

        with open("log/error_log.txt", 'a') as logfile:
            logfile.write("\n\n" + err_str)
