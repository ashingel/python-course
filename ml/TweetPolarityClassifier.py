import random
import textblob


class TweetPolarityClassifier:

    # method classifying list of twitter messages
    # input data is a list of Tweet objects
    def classify_tweets(self, tweets):
        for tweet in tweets:
            tweet_text = tweet.twitter_text
            polarity, intensity, probability = self.classify_text(tweet_text)
            tweet.polarity = polarity
            tweet.intensity = intensity
            tweet.probability = probability

    def classify_text(self, tweet_text):

        analysis = textblob.TextBlob(tweet_text)
        sentiment = analysis.sentiment
        polarity = "neutral"
        if analysis.sentiment[0] > 0:
            polarity = "positive"
        elif analysis.sentiment[0] < 0:
            polarity = "negative"

        # polarity_rand = ["positive", "negative", "neutral"]
        # polarity = polarity_rand[random.randint(0, 2)]

        # intensity_rand = ["high", "low", "medium"]
        # intensity = intensity_rand[random.randint(0, 2)]

        return polarity, random.uniform(0, 1), random.uniform(0.5, 1)
