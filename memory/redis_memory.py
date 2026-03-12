import redis
import json
from config import settings, logger

class RedisMemory:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.ttl = 3600  # 1 hour session TTL

    def set_session(self, session_id: str, data: dict):
        try:
            self.redis_client.setex(session_id, self.ttl, json.dumps(data))
            logger.info(f"Session {session_id} saved in Redis")
        except Exception as e:
            logger.error(f"Failed to save session {session_id}: {e}")

    def get_session(self, session_id: str) -> dict:
        try:
            data = self.redis_client.get(session_id)
            if data:
                return json.loads(data)
            return {}
        except Exception as e:
            logger.error(f"Failed to fetch session {session_id}: {e}")
            return {}

    def update_session(self, session_id: str, new_data: dict):
        session_data = self.get_session(session_id)
        session_data.update(new_data)
        self.set_session(session_id, session_data)

    def delete_session(self, session_id: str):
        try:
            self.redis_client.delete(session_id)
            logger.info(f"Session {session_id} deleted from Redis")
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")