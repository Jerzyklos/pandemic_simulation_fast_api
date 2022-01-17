import pymongo
import secret


class MongoDB:

    def __init__(self):
        url = secret.url
        self.client = pymongo.MongoClient(url)
        self.db = self.client["simulation_db"]
        self.col_persons = self.db["simulation_persons"]
        self.col_stats = self.db["simulation_statistics"]

    def delete_collection_content(self):
        self.col_persons.delete_many({})
        self.col_stats.delete_many({})

    def add_persons_to_col(self, data):
        self.col_persons.insert_one(data)

    def add_stats_to_col(self, data):
        self.col_stats.insert_one(data)

    def return_record(self):
        # return self.collection.find_one()
        return self.col_persons.find()

    def print_info(self):
        print(self.client.list_database_names())
        print(self.db.list_collection_names())
