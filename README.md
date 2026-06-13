# E-Commerce Query Chatbot

An AI-powered **E-Commerce Query Chatbot** built using **LangGraph, LangChain, Groq LLM, SQLite, and SQLAlchemy**. The chatbot handles customer support tasks such as **order tracking, product queries, returns/refunds, and personalized recommendations** through a modular multi-agent workflow.

---

## Features

* 🚚 **Order Status Tracking**

  * Track customer orders
  * Show shipping and delivery status
  * Handle multiple order clarification

* 🛍️ **Product Query Handling**

  * Check product availability
  * View product price and ratings
  * Suggest alternatives for out-of-stock items

* ↩️ **Returns & Refund Support**

  * Check refund status
  * Handle return requests
  * Validate return eligibility

* ⭐ **Product Recommendations**

  * Personalized suggestions
  * Budget-based recommendations
  * Category-based filtering

* 🧠 **AI Agent Workflow**

  * Multi-agent architecture using LangGraph
  * Intent classification-based routing
  * Follow-up conversational memory

* 📊 **Observability & Evaluation**

  * LangSmith tracing support
  * Evaluation dataset for intent accuracy

---

## Tech Stack

### Languages & Frameworks

* Python
* LangChain
* LangGraph

### Database

* SQLite
* SQLAlchemy

### AI / LLM

* Groq API (`llama-3.1-8b-instant`)

### Other Tools

* Faker
* LangSmith
* python-dotenv

---

## Project Structure

```bash
ecommerce-chatbot/
│── agent/
│   ├── __init__.py
│   ├── db_tool.py
│   ├── graph.py
│   ├── state.py
│   └── nodes/
│       ├── fallback.py
│       ├── greeting.py
│       ├── intent_classifier.py
│       ├── order_status.py
│       ├── product_query.py
│       ├── recommendation.py
│       └── returns.py
│
│── evals/
│   ├── dataset.json
│   └── run_evals.py
│
│── main.py
│── seed_db.py
│── requirements.txt
│── .env
│── ecommerce.db
│── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ecommerce-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ecommerce-chatbot
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

---

## Running the Project

### Step 1: Seed the Database

Generate sample customers, products, orders, and returns:

```bash
python seed_db.py
```

### Step 2: Run the Chatbot

```bash
python main.py
```

Example queries:

```text
Where is my order?
Can I return my product?
Recommend products under 1000
Is the laptop in stock?
```

### Step 3: Run Evaluations

```bash
python evals/run_evals.py
```

---

## LangGraph Workflow

The chatbot follows a **state-machine architecture**:

```text
User Input
      ↓
Intent Classifier
      ↓
 ┌───────────────┬──────────────┬─────────────┐
 ↓               ↓              ↓             ↓
Order Status  Product Query   Returns   Recommendation
      ↓
Fallback / Escalation (if needed)
```

The chatbot maintains **follow-up context** to support multi-turn conversations.

Example:

```text
User: Where is my order?
Bot: Which order do you mean?

User: O0001
Bot: Your order is shipped.

User: Can I return it?
Bot: Yes, your order is eligible for return.
```

---

## Evaluation

The chatbot uses an evaluation dataset to test intent classification accuracy.

Covered intents:

* Order Status
* Product Query
* Returns
* Recommendation
* Greeting
* Fallback

Run evaluation:

```bash
python evals/run_evals.py
```

---

## Challenges Faced

* Managing follow-up conversational context
* Intent routing inconsistencies
* Prompt tuning for reliable classification
* Multi-turn state management
* Debugging with LangSmith traces

---

## Future Improvements

* Add payment/order cancellation support
* Improve recommendation quality
* Add authentication system
* Deploy as a web application
* Add vector search for products

---



Just copy this into **README.md** in VS Code and push to GitHub. It looks professional for internship/project submissions.
