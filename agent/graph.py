from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.intent_classifier import intent_classifier_node
from agent.nodes.order_status import order_status_node
from agent.nodes.product_query import product_query_node
from agent.nodes.returns import returns_node
from agent.nodes.recommendation import recommendation_node
from agent.nodes.fallback import fallback_node
from agent.nodes.greeting import greeting_node


def route_intent(state):
    if state.get("escalation_flag"):
        return "fallback"

    intent = state.get("intent", "fallback")

    mapping = {
        "order_status"  : "order_status",
        "product_query" : "product_query",
        "returns"       : "returns",
        "recommendation": "recommendation",
        "greeting"      : "greeting",
        "fallback"      : "fallback",
    }
    return mapping.get(intent, "fallback")


builder = StateGraph(AgentState)

builder.add_node("intent_classifier", intent_classifier_node)
builder.add_node("order_status",      order_status_node)
builder.add_node("product_query",     product_query_node)
builder.add_node("returns",           returns_node)
builder.add_node("recommendation",    recommendation_node)
builder.add_node("fallback",          fallback_node)
builder.add_node("greeting",          greeting_node)

builder.set_entry_point("intent_classifier")

builder.add_conditional_edges(
    "intent_classifier",
    route_intent,
    {
        "order_status"  : "order_status",
        "product_query" : "product_query",
        "returns"       : "returns",
        "recommendation": "recommendation",
        "greeting"      : "greeting",
        "fallback"      : "fallback",
    }
)

for node in ["order_status", "product_query", "returns",
             "recommendation", "fallback", "greeting"]:
    builder.add_edge(node, END)

graph = builder.compile()