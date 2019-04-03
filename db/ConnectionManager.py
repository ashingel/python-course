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

    def add_record(self, user_name):
        sql = "INSERT INTO tweets(user_name) VALUES ('" + user_name + "')"
        try:
            self.connection.execute(sql)
            self.connection.commit()
        except Exception as ex:
            print(ex)

    def add_records(self, column_name, records):
        sql = "INSERT INTO test(" + column_name + ") VALUES (?)"
        try:
            records_to_add = [tuple(s.split()) for s in records]

            self.connection.executemany(sql, records_to_add)
            self.connection.commit()
        except Exception as ex:
            print(ex)

    def add_simple_records(self, column_name, records):
        sql = "INSERT INTO test (" + column_name + ") VALUES (?)"
        try:
            for record in records:
                self.connection.execute(sql, (record,))
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
