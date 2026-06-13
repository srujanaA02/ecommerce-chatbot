from typing import List, Dict, Any
from typing_extensions import TypedDict


class AgentState(TypedDict):
    customer_id: str
    messages: List[Any]
    intent: str
    active_sub_agent: str
    db_query_results: Dict
    follow_up_context: Dict
    escalation_flag: bool
    turn_count: int
    consecutive_unresolved: int
    last_intent: str