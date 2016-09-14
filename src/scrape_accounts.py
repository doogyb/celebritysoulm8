import requests
from bs4 import BeautifulSoup
import bs4
import json
from twitter import *
import langdetect

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
        consumer_key = open("../keys/consumer-key.txt").read().strip()
        consumer_secret = open("../keys/consumer-secret.txt").read().strip()
        access_token = open("../keys/access-token.txt").read().strip()
        access_token_secret = open("../keys/access-token-secret.txt").read().strip()

        twitter = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

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

    # Handles already looked up:

    already_searched = json.load(open("../db/already-searched.json"))
    db = json.load(open("../db/top-handles.json", 'r'))
    non_english = json.load(open('../db/non-english-handles.json'))

    print len(already_searched)

    consumer_key = open("../keys/consumer-key.txt").read().strip()
    consumer_secret = open("../keys/consumer-secret.txt").read().strip()
    access_token = open("../keys/access-token.txt").read().strip()
    access_token_secret = open("../keys/access-token-secret.txt").read().strip()

    twitter = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

    for handle in db.keys():

        # multiple passes needed for twitter rate limits
        if handle not in already_searched:

            # iterate through db of handles, look up tweets and concatenate to form
            # a large enough data set, roughly 100 tweets

            try:
                info = twitter.statuses.user_timeline(screen_name=handle[1:], count=100)
                text_data = "\n".join([txt['text'] for txt in info])
                language = langdetect.detect(text_data)

                print handle
                already_searched.append(handle)

                if language != "en":
                    non_english.append(handle)

            except TwitterHTTPError as twitter_error:
                print "Failed at: " + handle
                print twitter_error
                break

    print "Writing to file..."
    fp = open("../db/already-searched.json", 'w')
    json.dump(already_searched, fp, indent=4)
    fp = open("../db/non-english-handles.json", 'w')
    json.dump(non_english, fp, indent=4)
