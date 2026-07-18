import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_core.tools import tool
from database.db_queries import create_ticket, update_ticket_status

@tool
def escalate_issue(order_id: str, customer_id: str, issue_description: str) -> dict:
    """Escalate a customer issue to a human manager. This creates an escalated support ticket."""
    full_description = f"Order: {order_id} - {issue_description}"
    ticket = create_ticket(customer_id, full_description)
    if ticket:
        update_ticket_status(ticket['ticket_id'], escalated=True)
        return {"status": "success", "message": "Issue has been escalated to a human agent.", "ticket_id": ticket['ticket_id']}
    return {"error": "Failed to escalate issue."}
