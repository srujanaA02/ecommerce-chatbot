import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from agent.graph import graph

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.json")

with open(DATASET_PATH) as f:
    dataset = json.load(f)

correct = 0
total = len(dataset)

print("=" * 65)
print("  Running Evaluation Suite")
print("=" * 65)

for i, item in enumerate(dataset, 1):
    state = {
        "customer_id": "C0001",
        "messages": [HumanMessage(content=item["query"])],
        "intent": "",
        "active_sub_agent": "",
        "db_query_results": {},
        "follow_up_context": {},
        "escalation_flag": False,
        "turn_count": 0,
        "consecutive_unresolved": 0,
        "last_intent": ""
    }

    try:
        result = graph.invoke(state)
        predicted = result["intent"]
    except Exception as e:
        predicted = "error"
        print(f"  ERROR on query {i}: {e}")

    expected = item["expected_intent"]
    match = predicted == expected
    correct += int(match)

    icon = "✅" if match else "❌"
    print(
        f"{icon} [{i:02d}] "
        f"Query: {item['query'][:40]:<40} | "
        f"Expected: {expected:<15} | "
        f"Got: {predicted}"
    )

print("=" * 65)
pct = correct / total * 100
print(f"  Accuracy: {correct}/{total} = {pct:.1f}%")
print("=" * 65)

if pct == 100.0:
    print("  🎉 Perfect score!")
elif pct >= 80.0:
    print("  ✅ Good accuracy!")
else:
    print("  ⚠️  Needs improvement.")