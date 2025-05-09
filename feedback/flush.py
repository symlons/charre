from feedback.mongo import MONGO_DB, MongoCollections, get_collection

if __name__ == "__main__":
    for collection in MongoCollections:
        client = get_collection(collection)
        client.drop()
        print(f"Dropped collection {collection.value} from database {MONGO_DB}")
