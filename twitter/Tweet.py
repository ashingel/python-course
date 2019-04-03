class Tweet:
    def __init__(self, tweet, user):
        super().__init__()
        self.twitter_text = tweet.text
        self.name = user.screen_name
        self.tweet_id = user.id
        self.creation_date = tweet.created_at
