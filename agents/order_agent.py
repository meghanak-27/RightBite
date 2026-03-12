import json
from utils.gemini_client import call_gemini
from config import logger


class OrderAgent:

    def create_order(self, user_order, menu_items):

        prompt = f"""
        Convert user order into structured JSON.

        User message:
        {user_order}

        Menu reference:
        {menu_items}

        Return JSON:
        {{
            "items": [
                {{
                    "name": "",
                    "qty": 1,
                    "modifiers": []
                }}
            ],
            "special_instructions": ""
        }}
        """

        try:

            response = call_gemini(prompt)

            order = json.loads(response)

            return order

        except Exception as e:

            logger.error(f"Order agent failed: {e}")

            return {"items": []}