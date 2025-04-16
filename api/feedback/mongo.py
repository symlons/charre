import os
from enum import Enum
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.collection import Collection

MONGO_DB = os.getenv("MONGO_DB", "charre")


class MongoCollections(Enum):
    LABELS = os.getenv("MONGO_LABELS", "labels")
    FEEDBACK = os.getenv("MONGO_FEEDBACK", "feedback")


def get_client(collection: Collection) -> Collection:
    """
    Returns a mongo client for a given collection

    :param collection: the collection to get the client for
    """
    return MongoClient(
        host=os.getenv("MONGO_HOST", "localhost"),
        port=int(os.getenv("MONGO_PORT", "27017")),
        username=os.getenv("MONGO_USERNAME", "mongo"),
        password=quote_plus(os.getenv("MONGO_PASSWORD", "mongo")),
        maxPoolSize=10,
        waitQueueTimeoutMS=2000,
    )[MONGO_DB][collection.value]
