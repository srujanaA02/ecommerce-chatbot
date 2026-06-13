import os
import sys

print("Loading env...")
from dotenv import load_dotenv
load_dotenv()

print("Importing graph...")
from langchain_core.messages import HumanMessage
from agent.graph import graph
print("Graph imported successfully")


def run_chat(customer_id: str = "C0001"):
    state = {
        "customer_id": customer_id,
        "messages": [],
        "intent": "",
        "active_sub_agent": "",
        "db_query_results": {},
        "follow_up_context": {},
        "escalation_flag": False,
        "turn_count": 0,
        "consecutive_unresolved": 0,
        "last_intent": ""
    }

    print("=" * 50)
    print(f"E-Commerce Chatbot  |  Customer: {customer_id}")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye! 👋")
            break
        if not user_input:
            continue

        state["messages"].append(HumanMessage(content=user_input))

        print("Invoking graph...")
        try:
            state = graph.invoke(state)
            last_msg = state["messages"][-1].content
            print(f"\nBot: {last_msg}")
            print(f"     [Intent: {state['intent']} | Agent: {state['active_sub_agent']}]")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else "C0001"
    run_chat(cid)