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
    ("system", """You are a product information assistant for an e-commerce platform.
Use the database results to answer the customer's product query.

RULES:
- In stock: Return product name, price, rating, and stock count.
- Out of stock: Say it's unavailable and suggest 1-2 alternatives from same category.
- Not found: Suggest the closest matching product by name.
- Multiple matches: List them briefly and ask for clarification.

Context: {context}
Database Results: {db_results}

Be concise. Keep response under 120 words."""),
    ("human", "{input}")
])

chain = prompt | llm


def product_query_node(state):
    last_msg = state["messages"][-1].content
    context = state.get("follow_up_context", {})

    products = query_db("""
        SELECT product_id, name, category, price, stock, rating
        FROM products
        ORDER BY rating DESC
    """)

    response = chain.invoke({
        "db_results": str(products),
        "context": str(context),
        "input": last_msg
    })

    print(f"[ProductQuery] queried {len(products)} products")

    return {
        **state,
        "db_query_results": {"products": products},
        "active_sub_agent": "product_query",
        "messages": state["messages"] + [AIMessage(content=response.content)]
    }