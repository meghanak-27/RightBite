# agents/menu_agent.py
from utils.gemini_client import query_gemini

class MenuAgent:
    def recommend_items(self, user_profile=None):
        menu_data = ["Margherita Pizza", "Pepperoni Pizza", "Veggie Burger", "Pasta Alfredo"]
        prompt = f"""
        User profile: {user_profile}
        Menu options: {menu_data}
        Suggest top 3 food items for this user in JSON format like: {{"recommended_items": []}}
        """
        response_text = query_gemini(prompt)
        # Gemini returns string, try to extract JSON safely
        try:
            import json
            return json.loads(response_text)
        except:
            return {"recommended_items": [item.strip() for item in menu_data[:3]]}