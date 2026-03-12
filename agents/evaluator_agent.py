import json
from utils.gemini_client import call_gemini
from config import logger


class EvaluatorAgent:

    def validate_responses(self, agent_responses):
        """
        Check correctness and consistency of all agent outputs.
        """

        prompt = f"""
        You are an evaluator agent.

        Agent responses: {agent_responses}

        Validate correctness and return JSON:
        {{
            "valid": true,
            "issues": [],
            "notes": ""
        }}
        """

        try:
            response = call_gemini(prompt)
            result = json.loads(response)
            return result
        except Exception as e:
            logger.error(f"Evaluator agent failed: {e}")
            return {"valid": False, "issues": ["Failed to validate"], "notes": ""}