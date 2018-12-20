import json

class DBDetails(object):

    DB_NAME = ""
    DB_HOST = ""
    DB_PASS = ""
    DB_USER = ""
    DB_PORT = 5432

    def __init__(self):
        with open('db.json') as json_data:
            d = json.loads(json_data.read())
            self.DB_NAME = d['dbname']
            self.DB_HOST = d['hostname']
            self.DB_PASS = d['password']
            self.DB_USER = d['username']
            self.DB_PORT = d['port']
    