import requests
from bs4 import BeautifulSoup
import bs4
import json

# Scraping the handles of the top 1000 followers
# Pages are separated by groups of 100 users


class TwitterHandle:
    def __init__(self, handle, name, following, followers, tweets):
        self.handle = handle
        self.name = name
        self.following = following
        self.followers = followers
        self.tweets = tweets


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

        leaderboard = soup.find("ol", {"id" : "leaderboard"})


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
    with open("../db/top-1000-handles.json", "w") as fp:
        json.dump(users, fp, indent=4)

scrape()


