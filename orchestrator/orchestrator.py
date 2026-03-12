# import uuid
# from typing import TypedDict, Optional
# import json
# from langgraph.graph import StateGraph, END
# from agents import IntentAgent, MenuAgent, OrderAgent, PaymentAgent, DeliveryAgent, EvaluatorAgent
# from memory import RedisMemory, LongTermMemory
# from config import logger


# from agents import (
#     IntentAgent,
#     MenuAgent,
#     OrderAgent,
#     PaymentAgent,
#     DeliveryAgent,
#     EvaluatorAgent
# )

# from memory import RedisMemory, LongTermMemory
# from config import logger

# # -----------------------------
# # Graph State
# # -----------------------------
# class AgentState(TypedDict):
#     user_id: str
#     session_id: str
#     user_input: str

#     intent: Optional[str]

#     recommendations: Optional[dict]
#     order: Optional[dict]
#     payment: Optional[dict]
#     delivery: Optional[dict]

#     evaluation: Optional[dict]

#     response: Optional[str]


# # -----------------------------
# # Initialize Agents
# # -----------------------------
# intent_agent = IntentAgent()
# menu_agent = MenuAgent()
# order_agent = OrderAgent()
# payment_agent = PaymentAgent()
# delivery_agent = DeliveryAgent()
# evaluator_agent = EvaluatorAgent()

# # Memory
# redis_memory = RedisMemory()
# long_memory = LongTermMemory()


# # -----------------------------
# # Graph Nodes
# # -----------------------------

# def detect_intent(state: AgentState):

#     logger.info("Running Intent Agent")

#     result = intent_agent.classify_intent(state["user_input"])

#     state["intent"] = result.get("intent")

#     return state


# def recommend_menu(state: AgentState):

#     logger.info("Running Menu Agent")

#     user_profile = long_memory.get_user(state["user_id"])

#     menu_data = [
#         {"name": "Margherita Pizza", "price": 299},
#         {"name": "Veg Burger", "price": 149},
#         {"name": "Pasta Alfredo", "price": 249},
#         {"name": "Paneer Wrap", "price": 199}
#     ]

#     result = menu_agent.recommend_items(user_profile, menu_data)

#     state["recommendations"] = result

#     return state


# def create_order(state: AgentState):

#     logger.info("Running Order Agent")

#     menu_data = [
#         {"name": "Margherita Pizza", "price": 299},
#         {"name": "Veg Burger", "price": 149},
#         {"name": "Pasta Alfredo", "price": 249}
#     ]

#     order = order_agent.create_order(state["user_input"], menu_data)

#     state["order"] = order

#     return state


# def handle_payment(state: AgentState):

#     logger.info("Running Payment Agent")

#     user_profile = long_memory.get_user(state["user_id"])

#     payment = payment_agent.suggest_payment(state["order"], user_profile)

#     state["payment"] = payment

#     return state


# def track_delivery(state: AgentState):

#     logger.info("Running Delivery Agent")

#     order_id = str(uuid.uuid4())

#     delivery = delivery_agent.track_order("user_location", order_id)

#     state["delivery"] = delivery

#     return state


# def evaluate(state: AgentState):

#     logger.info("Running Evaluator Agent")

#     responses = {
#         "recommendations": state.get("recommendations"),
#         "order": state.get("order"),
#         "payment": state.get("payment"),
#         "delivery": state.get("delivery"),
#     }

#     evaluation = evaluator_agent.validate_responses(responses)

#     state["evaluation"] = evaluation

#     return state


# def generate_response(state: AgentState):

#     intent = state["intent"]

#     if intent == "order_food":
#         state["response"] = f"Order created: {state.get('order')}"

#     elif intent == "track_order":
#         state["response"] = f"Delivery Status: {state.get('delivery')}"

#     elif intent == "cancel_order":
#         state["response"] = "Your order has been cancelled."

#     else:
#         state["response"] = "Sorry, I didn't understand your request."

#     return state


# # -----------------------------
# # Router
# # -----------------------------
# def route_intent(state: AgentState):

#     intent = state["intent"]

#     if intent == "order_food":
#         return "menu"

#     if intent == "track_order":
#         return "delivery"

#     return "response"


# # -----------------------------
# # Build LangGraph
# # -----------------------------

# def build_graph():

#     graph = StateGraph(AgentState)

#     graph.add_node("intent", detect_intent)
#     graph.add_node("menu", recommend_menu)
#     graph.add_node("order", create_order)
#     graph.add_node("payment", handle_payment)
#     graph.add_node("delivery", track_delivery)
#     graph.add_node("evaluate", evaluate)
#     graph.add_node("response", generate_response)

#     graph.set_entry_point("intent")

#     graph.add_conditional_edges(
#         "intent",
#         route_intent,
#         {
#             "menu": "menu",
#             "delivery": "delivery",
#             "response": "response"
#         }
#     )

#     graph.add_edge("menu", "order")
#     graph.add_edge("order", "payment")
#     graph.add_edge("payment", "evaluate")
#     graph.add_edge("delivery", "evaluate")

#     graph.add_edge("evaluate", "response")
#     graph.add_edge("response", END)

#     return graph.compile()


# # -----------------------------
# # Orchestrator Class
# # -----------------------------

# class AgentOrchestrator:

#     def __init__(self):
#         self.graph = build_graph()

#     def run(self, user_id: str, session_id: str, user_input: str):

#         logger.info("Starting Agent Workflow")

#         state = {
#             "user_id": user_id,
#             "session_id": session_id,
#             "user_input": user_input
#         }

#         result = self.graph.invoke(state)

#         redis_memory.update_session(session_id, result)

#         return result["response"]


import uuid
from typing import TypedDict, Optional
import json
from langgraph.graph import StateGraph, END
from agents import IntentAgent, MenuAgent, OrderAgent, PaymentAgent, DeliveryAgent, EvaluatorAgent
from memory import RedisMemory, LongTermMemory
from config import logger


from agents import (
    IntentAgent,
    MenuAgent,
    OrderAgent,
    PaymentAgent,
    DeliveryAgent,
    EvaluatorAgent
)

from memory import RedisMemory, LongTermMemory
from config import logger

# -----------------------------
# Graph State
# -----------------------------
class AgentState(TypedDict):
    user_id: str
    session_id: str
    user_input: str

    intent: Optional[str]

    recommendations: Optional[dict]
    order: Optional[dict]
    payment: Optional[dict]
    delivery: Optional[dict]

    evaluation: Optional[dict]

    response: Optional[str]


# -----------------------------
# Initialize Agents
# -----------------------------
intent_agent = IntentAgent()
menu_agent = MenuAgent()
order_agent = OrderAgent()
payment_agent = PaymentAgent()
delivery_agent = DeliveryAgent()
evaluator_agent = EvaluatorAgent()

# Memory
redis_memory = RedisMemory()
long_memory = LongTermMemory()


# -----------------------------
# Graph Nodes
# -----------------------------

def detect_intent(state: AgentState):

    logger.info("Running Intent Agent")

    result = intent_agent.classify_intent(state["user_input"])

    state["intent"] = result.get("intent")

    return state


def recommend_menu(state: AgentState):

    logger.info("Running Menu Agent")

    user_profile = long_memory.get_user(state["user_id"])

    menu_data = [
        {"name": "Margherita Pizza", "price": 299},
        {"name": "Veg Burger", "price": 149},
        {"name": "Pasta Alfredo", "price": 249},
        {"name": "Paneer Wrap", "price": 199}
    ]

    result = menu_agent.recommend_items(user_profile, menu_data)

    state["recommendations"] = result

    return state


def create_order(state: AgentState):

    logger.info("Running Order Agent")

    menu_data = [
        {"name": "Margherita Pizza", "price": 299},
        {"name": "Veg Burger", "price": 149},
        {"name": "Pasta Alfredo", "price": 249}
    ]

    order = order_agent.create_order(state["user_input"], menu_data)

    state["order"] = order

    return state


def handle_payment(state: AgentState):

    logger.info("Running Payment Agent")

    user_profile = long_memory.get_user(state["user_id"])

    payment = payment_agent.suggest_payment(state["order"], user_profile)

    state["payment"] = payment

    return state


def track_delivery(state: AgentState):

    logger.info("Running Delivery Agent")

    order_id = str(uuid.uuid4())

    delivery = delivery_agent.track_order("user_location", order_id)

    state["delivery"] = delivery

    return state


def evaluate(state: AgentState):

    logger.info("Running Evaluator Agent")

    responses = {
        "recommendations": state.get("recommendations"),
        "order": state.get("order"),
        "payment": state.get("payment"),
        "delivery": state.get("delivery"),
    }

    evaluation = evaluator_agent.validate_responses(responses)

    state["evaluation"] = evaluation

    return state


def generate_response(state: AgentState):

    intent = state["intent"]

    if intent == "order_food":
        state["response"] = f"Order created: {state.get('order')}"

    elif intent == "track_order":
        state["response"] = f"Delivery Status: {state.get('delivery')}"

    elif intent == "cancel_order":
        state["response"] = "Your order has been cancelled."

    else:
        state["response"] = "Sorry, I didn't understand your request."

    return state


# -----------------------------
# Router
# -----------------------------
def route_intent(state: AgentState):

    intent = state["intent"]

    if intent == "order_food":
        return "menu"

    if intent == "track_order":
        return "delivery"

    return "response"


# -----------------------------
# Build LangGraph
# -----------------------------

def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("intent", detect_intent)
    graph.add_node("menu", recommend_menu)
    graph.add_node("order", create_order)
    graph.add_node("payment", handle_payment)
    graph.add_node("delivery", track_delivery)
    graph.add_node("evaluate", evaluate)
    graph.add_node("response", generate_response)

    graph.set_entry_point("intent")

    graph.add_conditional_edges(
        "intent",
        route_intent,
        {
            "menu": "menu",
            "delivery": "delivery",
            "response": "response"
        }
    )

    graph.add_edge("menu", "order")
    graph.add_edge("order", "payment")
    graph.add_edge("payment", "evaluate")
    graph.add_edge("delivery", "evaluate")

    graph.add_edge("evaluate", "response")
    graph.add_edge("response", END)

    return graph.compile()


# -----------------------------
# Orchestrator Class
# -----------------------------
# orchestrator/orchestrator.py
from agents import IntentAgent, MenuAgent, OrderAgent, PaymentAgent, DeliveryAgent, EvaluatorAgent

class AgentOrchestrator:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.menu_agent = MenuAgent()
        self.order_agent = OrderAgent()
        self.payment_agent = PaymentAgent()
        self.delivery_agent = DeliveryAgent()
        self.evaluator_agent = EvaluatorAgent()

    def handle_message(self, message, user_profile=None):
        # Step 1: Intent
        intent_result = self.intent_agent.detect_intent(message)

        # Step 2: Menu recommendations
        menu_result = self.menu_agent.recommend_items(user_profile=user_profile)

        # Step 3: Generate order
        order_result = self.order_agent.create_order(message, menu_result)

        # Step 4: Payment suggestions
        payment_result = self.payment_agent.suggest_payment(order_result, user_profile)

        # Step 5: Delivery info (mock)
        delivery_result = self.delivery_agent.track_order(order_id="12345", location="user_location")

        # Step 6: Validate all
        eval_result = self.evaluator_agent.validate_responses({
            "intent": intent_result,
            "menu": menu_result,
            "order": order_result,
            "payment": payment_result,
            "delivery": delivery_result
        })

        # Return combined JSON
        return {
            "intent": intent_result,
            "menu": menu_result,
            "order": order_result,
            "payment": payment_result,
            "delivery": delivery_result,
            "evaluation": eval_result
        }