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
    ("system", """You are a product recommendation assistant for an e-commerce platform.
Use the database results to suggest products to the customer.

RULES:
- Customer has order history: Recommend from categories they have NOT purchased yet.
- No order history: Recommend top-rated products overall.
- Budget specified in query: Only recommend products within that price range.
- Category specified in query: Filter by that category, rank by rating.
- Always return exactly 3-5 recommendations with: name, price, rating.

Customer ID: {customer_id}
Purchased Categories: {purchased_cats}
Top Products: {top_products}

Be friendly and enthusiastic. Keep response under 150 words."""),
    ("human", "{input}")
])

chain = prompt | llm


def recommendation_node(state):
    cid = state["customer_id"]
    last_msg = state["messages"][-1].content

    purchased_cats = query_db(f"""
        SELECT DISTINCT p.category
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.customer_id = '{cid}'
    """)

    top_products = query_db("""
        SELECT product_id, name, category, price, stock, rating
        FROM products
        WHERE stock > 0
        ORDER BY rating DESC
        LIMIT 30
    """)

    response = chain.invoke({
        "customer_id": cid,
        "purchased_cats": str(purchased_cats),
        "top_products": str(top_products),
        "input": last_msg
    })

    print(f"[Recommendation] generated suggestions for {cid}")

    return {
        **state,
        "db_query_results": {"recommendations": top_products},
        "active_sub_agent": "recommendation",
        "messages": state["messages"] + [AIMessage(content=response.content)]
    }