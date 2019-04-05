class Tweet:
    # polarity: positive/negative/neutral
    # intensity: low/medium/high
    polarity = "neutral"
    intensity = 0
    probability = 0

    def __init__(self, tweet, user):
        super().__init__()
        self.twitter_text = tweet.full_text
        self.name = user.screen_name
        self.tweet_id = user.id
        self.creation_date = tweet.created_at
