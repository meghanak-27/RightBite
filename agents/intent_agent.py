import json
from utils.gemini_client import call_gemini
from config import logger


class IntentAgent:

    def classify_intent(self, user_input: str):

        prompt = f"""
        Classify the intent.

        User message: {user_input}

        Possible intents:
        - order_food
        - track_order
        - cancel_order
        - unknown

        Return JSON:
        {{
            "intent": "",
            "confidence": 0-1
        }}
        """

        try:

            response = call_gemini(prompt)

            result = json.loads(response)

            logger.info(f"Intent detected: {result}")

            return result

        except Exception as e:

            logger.error(f"Intent agent failed: {e}")

            return {"intent": "unknown", "confidence": 0}