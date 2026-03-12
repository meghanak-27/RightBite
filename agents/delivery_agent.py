import json
from utils.gemini_client import call_gemini
from config import logger


class DeliveryAgent:

    def track_order(self, order_id, location):
        """
        Provide ETA and status based on order ID and location.
        """

        prompt = f"""
        You are a delivery assistant.

        Order ID: {order_id}
        User location: {location}

        Return JSON like:
        {{
            "delivery_status": "on the way",
            "ETA_minutes": 30,
            "notes": ""
        }}
        """

        try:
            response = call_gemini(prompt)
            result = json.loads(response)
            return result
        except Exception as e:
            logger.error(f"Delivery agent failed: {e}")
            return {"delivery_status": "unknown", "ETA_minutes": 0, "notes": "Failed to generate ETA"}