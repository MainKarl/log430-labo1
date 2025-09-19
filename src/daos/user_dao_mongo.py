import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.user import User

class UserDAOMongo:
    def __init__(self):
        try:
            env_path=".env"
            print(os.path.abspath(env_path))
            load_dotenv(dotenv_path=env_path)
            db_name = os.getenv("MONGODB_NAME")
            db_uri = os.getenv("MONGODB_URL")
            client = MongoClient(db_uri)

            database = client[db_name]
            self.users = database["users"]

        except FileNotFoundError as e:
            print("Attention: Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur: "+str(e))

    def select_all(self):
        return [User(str(row["_id"]), row["name"], row["email"]) for row in self.users.find()]

    def insert(self, user):
        insert_operation = { "name": user.name, "email": user.email }
        result = self.users.insert_one(insert_operation)
        return result.inserted_id

    def update(self, user):
        query_filter = { "_id": user.id }
        update_operation = { "$set" : {"name" : user.name, "email" : user.email }}
        self.users.update_one(query_filter, update_operation)
    
    def delete(self, user_id):
        query_filter = { "_id": user_id }
        self.users.delete_one(query_filter)

    def delete_all(self):
        self.users.delete_many()