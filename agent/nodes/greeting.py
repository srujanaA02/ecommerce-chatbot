from langchain_core.messages import AIMessage


def greeting_node(state):
    msg = (
        "Hello! 👋 Welcome to E-Commerce Support!\n\n"
        "I can help you with:\n"
        "  🚚 Order Status     - Track your orders\n"
        "  🛍️  Products        - Check price, stock, details\n"
        "  ↩️  Returns         - Start a return or check refund\n"
        "  ⭐ Recommendations  - Get personalized suggestions\n\n"
        "What can I help you with today?"
    )
    print("[Greeting] responding to greeting")

    return {
        **state,
        "active_sub_agent": "greeting",
        "messages": state["messages"] + [AIMessage(content=msg)]
    }