import twitter
import os


def get_url_image_of_user(handle):

    t = twitter.Api(*auth_twitter())
    user = t.UsersLookup(screen_name=handle)
    return user[0].profile_image_url.replace("_normal", "")


def delete_all_tweets():

    t = twitter.Api(*auth_twitter())
    timeline = t.GetUserTimeline(screen_name='celebritysoulm8')
    print((len(timeline)))

    for tweet in timeline:

        print("Destroying: ", tweet.text)
        t.DestroyStatus(t.id)


def auth_twitter():

    consumer_key = os.environ['CELEBRITYSOULM8_CONSUMER']
    consumer_secret = os.environ['CELEBRITYSOULM8_CONSUMER_SECRET']
    access_token = os.environ['CELEBRITYSOULM8_ACCESS']
    access_token_secret = os.environ['CELEBRITYSOULM8_ACCESS_SECRET']

    return consumer_key, consumer_secret, access_token, access_token_secret


if __name__ == "__main__":
    pass
