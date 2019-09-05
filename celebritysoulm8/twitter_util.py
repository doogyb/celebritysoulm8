import twitter


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

    consumer_key = open("keys/consumer-key.txt").read().strip()
    consumer_secret = open("keys/consumer-secret.txt").read().strip()
    access_token = open("keys/access-token.txt").read().strip()
    access_token_secret = open("keys/access-secret.txt").read().strip()

    return consumer_key, consumer_secret, access_token, access_token_secret


if __name__ == "__main__":
    pass
