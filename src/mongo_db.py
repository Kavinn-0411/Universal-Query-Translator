from pymongo import MongoClient
import pprint

def mongo_engine(username='',password=''):
    if username == '' and password == '':
        conn_string = 'mongodb://localhost:27017'
    else:
        conn_string = 'fmongodb://{username}:{password}@localhost:27017'

    with MongoClient(conn_string) as client:
        try:
            client.admin.command('ismaster')
            print("MongoDB connection successful")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            exit()

    client = MongoClient(conn_string)
    return client

# username, password = '',''
# client = testMongo(username,password)

def mongo_schema(client):
    def get_user_dbs():
        user_db_list = []
        master_db_list = client.list_database_names()

        for db in master_db_list:
            if db in ['admin','config','local']:
                continue
            user_db_list.append(db)

        return user_db_list

    user_db_list = get_user_dbs()
    # print(user_db_list)

    def get_db_collection_dict(db_list):
        db_collection_dict ={}

        for db_name in db_list:
            db = client[db_name]
            collections = db.list_collection_names()
            db_collection_dict[db_name] = collections

        return db_collection_dict

    db_collection_dict = get_db_collection_dict(user_db_list)
    # print(db_collection_dict)

    def get_collection_definitions(db_collection_dict):
        collection_definitions = ''
        for db_name,collection_list in db_collection_dict.items():
            db = client[db_name]

            for collection in collection_list:
                documents = list(db[collection].aggregate([{"$sample": {"size": 5}}]))

                if documents is None:
                    continue
                
                collection_definitions += f'\nDatabase: {db_name}\n' + f'Collection: {collection}\n' + f'Random 5 Documents in the collection {collection} stored in the database {db_name}:\n' 
                for document in documents:
                    collection_definitions +=  f'{document}\n'
        
        return collection_definitions


    collection_definitions = get_collection_definitions(db_collection_dict)
    # print(collection_definitions)
    return collection_definitions



