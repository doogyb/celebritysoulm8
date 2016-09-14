import requests
from bs4 import BeautifulSoup
import bs4
import json
from twitter import *
import langdetect

from twitterbot import auth_twitter

# Scraping the handles of the top 1000 followers
# Pages are separated by groups of 100 users


def scrape():
    users = {}
    for i in range(10):
        if i == 0:
            url = "http://twittercounter.com/pages/100/"
        else:
            url = "http://twittercounter.com/pages/100/" + str(i*100)

        print url
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        leaderboard = soup.find("ol", {"id": "leaderboard"})

        for child in leaderboard.children:
            if type(child) is bs4.element.Tag:
                handle = child.find_all("span", {"itemprop" : "alternateName"})
                name = child.find_all("span", {"itemprop": "name"})
                # Dirty, but it works
                try:
                    followers = child.find_all("div", class_="num-followers active")[0].\
                        find("span", class_="num").string.replace(",", "")
                    following = child.find_all("div", class_="num-following inactive")[0].\
                        find("span", class_="num").string.replace(",", "")
                    tweets = child.find_all("div", class_="num-following inactive")[1].\
                        find("span", class_="num").string.replace(",", "")
                except:
                    print "Can't match"

                if len(handle) > 0:
                    # save to dictionary
                    users[handle[0].string] = {"Name": name[0].string, "Following": int(following),
                                               "Followers": int(followers), "Tweets": int(tweets)}

    print len(users)
    with open("../db/top-handles.json", "w") as fp:
        json.dump(users, fp, indent=4)


def remove_non_english_users(lookup=False):
    # function which looks up users language
    # and removes if not english.

    if lookup:

        twitter = Twitter(auth=auth_twitter())

        db = json.load(open("../db/top-handles.json", 'r'))

        # iterate over groups of 99 in order to make less requests, then
        # search for language and remove if not en

        non_english = []

        for i in range(0, 1000, 99):
            try:
                users = twitter.users.lookup(screen_name=",".join([handle[1:] for handle in db.keys()[i:i+99]]))
            except:
                print "Messed up with: ", ",".join([handle[1:] for handle in db.keys()[i:i+99]])

            for user in users:
                if user['lang'] != "en" and user['lang'] != "en-gb":
                    print "Removing " + user['screen_name'] + " : " + user['lang']
                    non_english.append("@" + user['screen_name'])

        fp = open("../db/non-english-handles.json", 'w')
        json.dump(non_english, fp, indent=4)

    non_english = json.load(open("../db/non-english-handles.json"))
    db = json.load(open("../db/top-handles.json"))
    for user in non_english:
        if user not in db:
            print "Key error with " + user
        else:
            db.pop(user)

    fp = open("../db/temp.json", 'w')
    json.dump(db, fp, indent=4)


def remove_non_english_by_detection():
    # This method attempts to detect the language
    # Contained in the users tweets using the langdetect module
    # and remove non english users from the database

    db = json.load(open("../db/all-handles.json", 'r'))

    # Handles already looked up:

    already_searched = json.load(open("../db/already-searched.json"))
    non_english = json.load(open('../db/non-english-handles.json'))
    maybe = json.load(open('../db/maybe-english.json'))

    twitter = Twitter(auth=auth_twitter())

    requests = 0

    for handle in db.keys():

        # multiple passes needed for twitter rate limits
        if handle not in already_searched:

            # iterate through db of handles, look up tweets and concatenate to form
            # a large enough data set, roughly 100 tweets

            try:
                info = twitter.statuses.user_timeline(screen_name=handle[1:], count=100, include_rts=False)
                text_data = "\n".join([txt['text'] for txt in info])
                try:
                    languages = langdetect.detect_langs(text_data)
                except:
                    print "Failed to detect language at: " + handle
                    print text_data

                requests += 1

                print handle
                already_searched.append(handle)

                if has_english(languages):
                    # has english tweets, but to what extent?
                    prob = language_probability(languages)
                    if prob == 0:
                        print "English: " + handle + " ---> " + str(languages)
                    elif prob == 1:
                        print "Maybe: " + handle + " ---> " + str(languages)
                        maybe.append(handle)

                    else:
                        print "Non english: " + handle + " ---> " + str(languages)
                else:
                    # has no english tweets
                    print "Non english: " + handle + " ---> " + str(languages)
                    non_english.append(handle)

            except TwitterHTTPError as twitter_error:
                print "Failed at: " + handle
                print twitter_error
                print "\n\n\n Requests made: " + str(requests)
                break

    print "Writing to file..."
    fp = open("../db/already-searched.json", 'w')
    json.dump(already_searched, fp, indent=4)
    fp = open("../db/non-english-handles.json", 'w')
    json.dump(non_english, fp, indent=4)
    fp = open("../db/maybe-english.json", 'w')
    json.dump(maybe, fp, indent=4)


def move_to_maybe():

    handles = json.load(open("../db/non-english-handles.json"))
    twitter = Twitter(auth=auth_twitter())
    new_handles = handles
    maybe = []

    for handle in handles:

        info = twitter.statuses.user_timeline(screen_name=handle[1:], count=100, include_rts=False)
        text_data = "\n".join([txt['text'] for txt in info])
        languages = langdetect.detect_langs(text_data)

        print languages
        if has_english(languages):
            prob = language_probability(languages)
            if prob == 0:
                print "Handle is probably english: " + handle
                new_handles.remove(handle)
            elif prob == 1:
                print "Maybe: " + handle
                maybe.append(handle)
                new_handles.remove(handle)
            else:
                print "No: " + handle

        fp = open("../db/maybe-english.json", 'w')
        json.dump(maybe, fp, indent=4)
        fp = open("../db/non-english-handles.json", 'w')
        json.dump(new_handles, fp, indent=4)


def has_english(languages, is_lang='en'):
    # Helper function for langdetect module:
    for lang in languages:
        if lang.lang == is_lang:
            return True

    return False


def language_probability(languages, is_lang='en'):

    for lang in languages:
        if lang.lang == 'en':
            if lang.prob >= 0.7:
                return 0
            elif 0.5 <= lang.prob < 0.7:
                return 1
            else:
                return 2

    return False


def remove_users():
    non_english_users = json.load(open("../db/non-english-handles.json"))
    all_handles = json.load(open("../db/all-handles.json"))
    for handle in non_english_users:
        all_handles.pop(handle)

    fp = open("english-users.json", 'w')
    json.dump(all_handles, fp, indent=4)

remove_users()






















