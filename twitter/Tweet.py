import preprocessor as p


class Tweet:
    # polarity: positive/negative/neutral
    # intensity: low/medium/high
    polarity = "neutral"
    intensity = 0
    probability = 0

    def __init__(self, tweet, user):
        super().__init__()
        p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.NUMBER)
        self.twitter_text = p.clean(tweet.full_text)
        self.name = user.screen_name
        self.tweet_id = user.id
        self.creation_date = tweet.created_at
