from langchain_core.messages import AIMessage


def fallback_node(state):
    consecutive = state.get("consecutive_unresolved", 0)
    escalation = state.get("escalation_flag", False)

    if escalation:
        msg = (
            "I'm sorry, I wasn't able to resolve your query after several attempts. "
            "I'm now connecting you to a human support agent who will assist you shortly. "
            f"Your session ID is: {state.get('customer_id', 'N/A')} | "
            f"Turn: {state.get('turn_count', 0)}. "
            "Please stay on the line!"
        )
        print(f"[Fallback] ESCALATION triggered for customer {state.get('customer_id')}")
    else:
        msg = (
            "I'm sorry, I can only help with order status, products, returns, "
            "and recommendations. Could you please rephrase your question? 😊"
        )
        print(f"[Fallback] normal fallback | consecutive={consecutive}")

    return {
        **state,
        "active_sub_agent": "fallback",
        "escalation_flag": escalation,
        "messages": state["messages"] + [AIMessage(content=msg)]
    }