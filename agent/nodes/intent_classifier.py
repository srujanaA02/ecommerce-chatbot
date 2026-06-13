import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",   # replaces decommissioned llama3-8b-8192
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an intent classifier for an e-commerce chatbot.
Classify the user message into exactly one of these intents:

order_status    - user asking about order tracking, shipping, delivery, package status
product_query   - user asking about product price, stock, availability, details, specifications
returns         - user asking about returns, refunds, sending items back, return approval, wrong item received
recommendation  - user asking for product suggestions, what to buy, recommendations, best products, ideas
greeting        - user saying hi, hello, hey, thanks, goodbye, or general small talk
fallback        - anything NOT related to e-commerce (weather, jokes, math, politics, gibberish, random text)

STRICT RULES:
- Reply with ONLY one word from the list above. No punctuation. No explanation. No quotes.
- return/refund queries are ALWAYS: returns
- Random text or off-topic = fallback
- "show me X category" without asking for suggestions = product_query
- "what should I buy" or "suggest something" = recommendation"""),
    ("human", "{message}")
])

chain = prompt | llm

VALID_INTENTS = [
    "order_status", "product_query", "returns",
    "recommendation", "greeting", "fallback"
]


def intent_classifier_node(state):
    last_msg = state["messages"][-1].content if state["messages"] else ""

    result = chain.invoke({"message": last_msg})
    raw = result.content.strip().lower()

    # Clean up LLM output
    intent = raw.split()[0] if raw else "fallback"
    intent = intent.strip('.,!?"\'')

    # Normalize aliases
    aliases = {
        "return_request": "returns",
        "return": "returns",
        "refund": "returns",
        "unknown": "fallback",
        "order": "order_status",
        "product": "product_query",
        "recommend": "recommendation",
    }
    intent = aliases.get(intent, intent)

    if intent not in VALID_INTENTS:
        intent = "fallback"

    last_intent = state.get("last_intent", "")
    consecutive = state.get("consecutive_unresolved", 0)

    # Track consecutive fallbacks for escalation
    if intent == "fallback" and last_intent == "fallback":
        consecutive += 1
    elif intent == "fallback":
        consecutive = 1
    else:
        consecutive = 0

    escalation = consecutive >= 3

    print(f"[IntentClassifier] intent={intent} | consecutive={consecutive} | escalate={escalation}")

    return {
        **state,
        "intent": intent,
        "last_intent": intent,
        "consecutive_unresolved": consecutive,
        "escalation_flag": escalation,
        "turn_count": state.get("turn_count", 0) + 1
    }