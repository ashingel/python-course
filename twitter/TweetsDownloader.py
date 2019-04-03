from configparser import RawConfigParser

import tweepy

from db.ConnectionManager import ConnectionManager
from twitter.Tweet import Tweet

from twitter import Tweet


class TweetsDownloader:

    def __init__(self) -> None:
        super().__init__()

        # init twitter reading settings
        config = RawConfigParser()
        # config.read("././resources/application.properties")
        config.read(
            "D:/projects/education/python/sources/course-work/sources/python-course/resources/application.properties")
        self.access_details = dict(config.items('Twitter Access Section'))

    # Method for reading simple timeline
    def get_tweet_messages(self):
        # get authentication data
        consumer_key = self.access_details["consumer.api.key"]
        consumer_secret = self.access_details["consumer.api.secret.key"]
        access_token = self.access_details["access.token"]
        access_token_secret = self.access_details["access.secret.token"]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        public_tweets = api.search(q="minsk", lang="en", since_id=ConnectionManager.STARTING_ID)

        tweets = list()

        for tweet in public_tweets:
            user = tweet.user
            tweet_obj = Tweet.Tweet(tweet, user)
            tweets.append(tweet_obj)

        return tweets


def test_twitter():
    tw_loader = TweetsDownloader()
    messages = tw_loader.get_tweet_messages()
    for message in messages:
        print(message.name)


test_twitter()
