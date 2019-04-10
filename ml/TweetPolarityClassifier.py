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

    # The polarity score is a float within the range [-1.0, 1.0].
    # The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
    def classify_text(self, tweet_text):

        analysis = textblob.TextBlob(tweet_text)

        polarity = "neutral"

        if analysis.sentiment[0] > 0:
            polarity = "positive"
        elif analysis.sentiment[0] < 0:
            polarity = "negative"

        intensity = analysis.sentiment[1]

        return polarity, intensity, analysis.polarity
