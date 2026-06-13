import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from agent.db_tool import query_db

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a returns specialist for an e-commerce platform.
Use the database results to handle return inquiries.

RULES:
- Return approved: Confirm refund amount and 5-7 business day timeline.
- Return pending: State the status is pending review.
- Return rejected: Explain it was rejected and offer escalation.
- No return found + order is delivered: Offer to initiate a return, ask for reason.
- No return found + order NOT delivered: Explain only delivered orders qualify for returns.
- No order found: Ask user to confirm their order ID.

Customer ID: {customer_id}
Previous context: {context}
Database Results: {db_results}

Be empathetic and helpful. Keep response under 120 words."""),
    ("human", "{input}")
])

chain = prompt | llm


def returns_node(state):
    cid = state["customer_id"]
    context = state.get("follow_up_context", {})
    last_msg = state["messages"][-1].content

    order_id = context.get("order_id", "")

    if order_id:
        returns = query_db(f"""
            SELECT r.return_id, r.reason, r.status, r.refund_amount,
                   o.status as order_status, p.name as product_name
            FROM returns r
            JOIN orders o ON r.order_id = o.order_id
            JOIN products p ON o.product_id = p.product_id
            WHERE r.order_id = '{order_id}'
        """)
        orders = query_db(f"""
            SELECT o.order_id, o.status, p.name as product_name
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE o.order_id = '{order_id}'
        """)
    else:
        returns = query_db(f"""
            SELECT r.return_id, r.reason, r.status, r.refund_amount,
                   o.order_id, o.status as order_status, p.name as product_name
            FROM returns r
            JOIN orders o ON r.order_id = o.order_id
            JOIN products p ON o.product_id = p.product_id
            WHERE o.customer_id = '{cid}'
        """)
        orders = query_db(f"""
            SELECT o.order_id, o.status, p.name as product_name
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE o.customer_id = '{cid}'
        """)

    response = chain.invoke({
        "db_results": str({"returns": returns, "orders": orders}),
        "context": str(context),
        "customer_id": cid,
        "input": last_msg
    })

    print(f"[Returns] found {len(returns)} returns, {len(orders)} orders for {cid}")

    return {
        **state,
        "db_query_results": {"returns": returns, "orders": orders},
        "active_sub_agent": "returns",
        "messages": state["messages"] + [AIMessage(content=response.content)]
    }