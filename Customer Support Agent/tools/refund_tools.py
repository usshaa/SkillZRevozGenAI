import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_core.tools import tool
from database.db_queries import get_order_status

@tool
def check_refund_eligibility(order_id: str) -> dict:
    """Check if an order is eligible for a refund."""
    order = get_order_status(order_id)
    if not order:
        return {"error": "Order not found.", "eligible": False}
        
    status = order.get("status", "").lower()
    if status == "delivered":
        return {"eligible": True, "reason": "Order was delivered and is eligible."}
    return {"eligible": False, "reason": f"Order status is {status}, cannot refund."}

@tool
def process_refund(order_id: str, amount: float) -> dict:
    """Process a refund for a given order ID and amount."""
    return {"status": "success", "message": f"Refund of {amount} processed for order {order_id}."}
