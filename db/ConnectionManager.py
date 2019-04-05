import sqlite3


# Class which is responsible for the saving data to DB
class ConnectionManager:
    # initial tweet ID. We will work wtth messages since this tweet
    STARTING_ID = "1113488068554756096"

    # create connection to DB
    def __init__(self, path_to_file) -> None:
        super().__init__()
        try:
            self.connection = sqlite3.connect(path_to_file)
        except Exception as ex:
            print(ex)

    # Execute SQL command
    def execute_sql_command(self, sql_command):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_command)
            self.connection.commit()
        except Exception as ex:
            print(ex)

    def fetch_record(self, column_name):
        result = list()
        sql = "SELECT {} FROM test".format(column_name)
        try:
            cursor = self.connection.cursor().execute(sql)
            for record in cursor:
                result.append(record)

        except Exception as ex:
            print(ex)

        return result

    # close connection
    def close_connection(self):
        self.connection.close()

    def save_messages(self, tweets):

        for tweet in tweets:
            try:
                id = tweet.tweet_id
                screen_name = tweet.name
                text = tweet.twitter_text
                date = tweet.creation_date
                polarity = tweet.polarity
                intensity = tweet.intensity
                probability = tweet.probability

                sql = "INSERT INTO tweets (tweet_id,tw_user_name,tw_text,tw_date,tw_polarity,probability,intensity) VALUES (?,?,?,?,?,?,?)"
                self.connection.execute(sql, (id, screen_name, text, date, polarity, intensity, probability))
            except Exception as ex:
                print(sql)
                print(ex)

        self.connection.commit()
