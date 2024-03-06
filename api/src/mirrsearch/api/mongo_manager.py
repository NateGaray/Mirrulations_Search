"""
Python module that establishes database connections. This class
follows the singleton design pattern to ensure there is never
more than one database connection open. A mock database instance
can also be created using this class.
"""
from pymongo import MongoClient
import mongomock

class MongoManager:
    """
    Class that manages the connection to a Mongo database running locally or
    a mock Mongo database
    """
    __instance = None
    __mock = False

    @staticmethod
    def get_instance():
        """
        Static method that returns the MongoDB client. It creates the client
        if it hasn't been created before, otherwise it returns the current
        connection.
        """
        return MongoManager.__instance

    @staticmethod
    def close_instance():
        """
        Static method that closes the database connection if there is currently one open.
        If there is no connection open, the method does nothing.
        """
        if MongoManager.__instance is not None and MongoManager.__mock is False:
            MongoManager.__instance.close()
            MongoManager.__instance = None
        elif MongoManager.__mock is True:
            MongoManager.__instance = None

    def __init__(self, mock=False):
        """
        Initializer method that ensures there is only ever one database connection open.
        """
        if MongoManager.__instance is not None:
            raise ConnectionException(message='''Error: a database client has already been
                established, another connection cannot be created without
                closing the other first''')
        if mock is True:
            MongoManager.__instance = mongomock.MongoClient()
            MongoManager.__mock = True
        else:
            MongoManager.__instance = MongoClient('localhost', 27017)

class ConnectionException(Exception):
    """
    Class that represents the exception that is thrown when there is
    an issue with establishing a connection to the database.
    """

    def __init__(self, message='Error: the connection to the database could not be established'):
        """
        Initializer that uses the message argument to raise the exception
        """
        self.message = message
        super().__init__(self.message)
