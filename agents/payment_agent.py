import json
from utils.gemini_client import call_gemini
from config import logger


class PaymentAgent:

    def suggest_payment(self, order_json, user_profile=None):
        """
        Suggest payment options based on order and user profile.
        """

        prompt = f"""
        You are a payment assistant.

        Order: {order_json}
        User profile: {user_profile}

        Suggest available payment options (e.g., UPI, Card, Wallet) 
        and return a JSON like:
        {{
            "payment_options": ["UPI", "Card"],
            "notes": ""
        }}
        """

        try:
            response = call_gemini(prompt)
            result = json.loads(response)
            return result
        except Exception as e:
            logger.error(f"Payment agent failed: {e}")
            return {"payment_options": [], "notes": "Failed to generate options"}