from pymongo import MongoClient

from config.server_environment import MONGO_HOSTNAME, MONGO_PORT


class MongoEngine:
    client = MongoClient(MONGO_HOSTNAME, MONGO_PORT)
    collection = ''
    engine = None

    def __new__(cls, *args, **kwargs):
        if not cls.engine:
            cls.engine = super(MongoEngine, cls).__new__(cls, *args, **kwargs)
        return cls.engine

    """
        Get the customers client.
    """
    def get_client(self):
        if self.collection != '':
            return self.client[self.collection]

        return None

    """
        Sets the collection name.
    """
    def set_collection_name(self, collection):
        self.collection = collection

    """
        Gets the current collection name.
    """
    def get_collection_name(self):
        return self.collection

    """
        Gets all collection names.
    """
    def get_collection_names(self):
        return self.get_client().list_database_names()

    """
        Drops a database.
    """
    def drop(self, dbname):
        self.client.drop_database(dbname)

    """
        Drops a collection.
    """
    def drop_collection(self, dbname, dbcollection):
        if dbname is not None and dbcollection is not None:
            self.client[dbname][dbcollection].drop()

    """
        Returns the current status of the Mongo client.
    """
    def status(self):
        info = self.client.server_info()
        return {
            'is_up': info['ok'] == 1.0,
            'data_usage': [db for db in self.client.list_databases()],
            'info': info
        }
