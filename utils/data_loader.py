import json
from pymongo import MongoClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings

def load_users():

    client = MongoClient(settings.MONGO_URL)
    db = client["foodbot"]
    users = db["users"]

    with open("data/sample_users.json") as f:
        data = json.load(f)

    for user in data:
        users.update_one(
            {"user_id": user["user_id"]},
            {"$set": user},
            upsert=True
        )

    print("Users inserted")


def load_menu():

    client = MongoClient(settings.MONGO_URL)
    db = client["foodbot"]
    menu = db["menu"]

    with open("data/menu.json") as f:
        data = json.load(f)

    for item in data:
        menu.update_one(
            {"id": item["id"]},
            {"$set": item},
            upsert=True
        )

    print("Menu inserted")


if __name__ == "__main__":
    load_users()
    load_menu()