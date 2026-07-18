import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.order_tools import lookup_order, lookup_customer_orders
from tools.refund_tools import check_refund_eligibility, process_refund
from tools.ticket_tools import open_support_ticket, escalate_ticket

def test_tool_schemas():
    assert lookup_order.name == "lookup_order"
    assert lookup_customer_orders.name == "lookup_customer_orders"
    assert check_refund_eligibility.name == "check_refund_eligibility"
    assert process_refund.name == "process_refund"
    assert open_support_ticket.name == "open_support_ticket"
    assert escalate_ticket.name == "escalate_ticket"
