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
    ("system", """You are an order status assistant for an e-commerce platform.
Use the database results to answer the customer query.

RULES:
- Single shipped order: Return tracking number and estimated delivery date.
- Single processing order: Return estimated delivery date only.
- Multiple active orders: List them briefly and ask which one the user means.
- Order not found: Ask user to confirm the order ID.
- Cancelled order: Confirm cancellation and mention refund if applicable.

Customer ID: {customer_id}
Previous context: {context}
Database Results: {db_results}

Be concise and friendly. Keep response under 100 words."""),
    ("human", "{input}")
])

chain = prompt | llm


def order_status_node(state):
    cid = state["customer_id"]
    context = state.get("follow_up_context", {})
    last_msg = state["messages"][-1].content

    orders = query_db(f"""
        SELECT o.order_id, o.status, o.tracking_number,
               strftime('%Y-%m-%d', o.estimated_delivery) as estimated_delivery,
               strftime('%Y-%m-%d', o.order_date) as order_date,
               p.name as product_name, p.price
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.customer_id = '{cid}'
        ORDER BY o.order_date DESC
    """)

    response = chain.invoke({
        "db_results": str(orders),
        "customer_id": cid,
        "context": str(context),
        "input": last_msg
    })

    # Update context if single active order found
    new_context = context.copy()
    active = [o for o in orders if o.get("status") not in ["delivered", "cancelled"]]
    if len(active) == 1:
        new_context["order_id"] = active[0]["order_id"]
        new_context["product_name"] = active[0]["product_name"]
        new_context["status"] = active[0]["status"]

    print(f"[OrderStatus] found {len(orders)} orders for {cid}")

    return {
        **state,
        "db_query_results": {"orders": orders},
        "follow_up_context": new_context,
        "active_sub_agent": "order_status",
        "messages": state["messages"] + [AIMessage(content=response.content)]
    }