import pymongo
from simulation import Person

class Statistics:
    pass

class MongoDB:
    def __init__(self, password):
        url = "mongodb+srv://user0000:pass{}@cluster0.n0awd.mongodb.net/" \
              "myFirstDatabase?retryWrites=true&w=majority".format(password)
        self.client = pymongo.MongoClient(url)
        self.db = self.client["simulation_db"]
        self.collection = self.db["simulation_persons"]
        self.collection = self.db["simulation_statistics"]
    def delete_collection_content(self):
        self.collection.delete_many({})
    def add_persons_to_col(self, person:Person):
        pass
    def add_stats_to_col(self, stats:Statistics):
        pass
    def return_record(self):
        return self.collection.find_one()
    def print_info(self):
        print(self.client.list_database_names())
        print(self.db.list_collection_names())


mongoDB = MongoDB('XXXX')
mongoDB.print_info()
mongoDB.delete_collection_content()
print(mongoDB.return_record())

"""

"""
