import pymysql
print(pymysql.__version__)


class Database:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "database": "bookmyshow",
            "user": "root",
            "password": "mysql@12345",
            "cursorclass" : pymysql.cursors.DictCursor
        }
    def get_connection(self):
        return pymysql.connect(**self.config)
        
