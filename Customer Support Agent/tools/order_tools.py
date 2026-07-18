import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_core.tools import tool
from database.db_queries import get_order_status, get_customer_orders

@tool
def lookup_order(order_id: str) -> dict:
    """Lookup an order by its ID."""
    order = get_order_status(order_id)
    if order:
        return order
    return {"error": f"Order {order_id} not found."}

@tool
def lookup_customer_orders(customer_id: str) -> list:
    """Lookup all orders for a specific customer."""
    orders = get_customer_orders(customer_id)
    return orders
