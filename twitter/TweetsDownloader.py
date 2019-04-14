from configparser import RawConfigParser
import preprocessor as twproprocessor

import tweepy

from db.ConnectionManager import ConnectionManager
from ml.TweetPolarityClassifier import TweetPolarityClassifier
from twitter.Tweet import Tweet

from twitter import Tweet


class TweetsDownloader:

    def __init__(self) -> None:
        super().__init__()

        # init twitter reading settings
        config = RawConfigParser()
        config.read("././resources/application.properties")
        self.access_details = dict(config.items('Twitter Access Section'))
        self.sentiments_config = dict(config.items('Sentiments Settings'))
        self.tweets_number = self.sentiments_config["tweets.to.download"]

    # Method for reading simple timeline
    def get_tweet_messages(self, query, since_date):
        # get authentication data
        consumer_key = self.access_details["consumer.api.key"]
        consumer_secret = self.access_details["consumer.api.secret.key"]
        access_token = self.access_details["access.token"]
        access_token_secret = self.access_details["access.secret.token"]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        # public_tweets = api.search(q="minsk", lang="en", since_id=ConnectionManager.STARTING_ID)

        query += " -filter:retweets"
        searched_tweets = tweepy.Cursor(api.search, q=query, count=int(self.tweets_number), include_entities=True,
                                        tweet_mode='extended',
                                        since=since_date, lang="en")

        tweets = list()

        for tweet in searched_tweets.items(int(self.tweets_number)):
            user = tweet.user
            tweet_obj = Tweet.Tweet(tweet, user)
            tweets.append(tweet_obj)

        return tweets


def test_twitter():
    tw_loader = TweetsDownloader()
    query = "lukashenko"
    # format '2019-04-04'
    since_date = '2019-04-09'
    messages = tw_loader.get_tweet_messages(query, since_date)
    for message in messages:
        print(message.name)

    path_to_db = "D:/projects/education/python/sources/course-work/sources/python-course/resources/tweets.db"

    classifier = TweetPolarityClassifier()
    classifier.classify_tweets(messages)

    connection_manager = ConnectionManager(path_to_db)
    connection_manager.save_messages(messages, query)

# test_twitter()
