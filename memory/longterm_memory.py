from pymongo import MongoClient
from config import settings, logger

class LongTermMemory:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URL)
        self.db = self.client["foodbot"]
        self.users = self.db["users"]
        self.orders = self.db["orders"]

    # ---------- User Profiles ----------
    def save_user(self, user_id: str, profile: dict):
        try:
            self.users.update_one({"user_id": user_id}, {"$set": profile}, upsert=True)
            logger.info(f"User {user_id} saved/updated in MongoDB")
        except Exception as e:
            logger.error(f"Failed to save user {user_id}: {e}")

    def get_user(self, user_id: str) -> dict:
        try:
            user = self.users.find_one({"user_id": user_id})
            return user if user else {}
        except Exception as e:
            logger.error(f"Failed to fetch user {user_id}: {e}")
            return {}

    # ---------- Orders ----------
    def save_order(self, order_id: str, order_data: dict):
        try:
            self.orders.update_one({"order_id": order_id}, {"$set": order_data}, upsert=True)
            logger.info(f"Order {order_id} saved/updated in MongoDB")
        except Exception as e:
            logger.error(f"Failed to save order {order_id}: {e}")

    def get_order(self, order_id: str) -> dict:
        try:
            order = self.orders.find_one({"order_id": order_id})
            return order if order else {}
        except Exception as e:
            logger.error(f"Failed to fetch order {order_id}: {e}")
            return {}