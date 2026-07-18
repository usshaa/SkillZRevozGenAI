import os
import sys
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.db_setup import get_engine, Customer, Order, Ticket

engine = get_engine()
Session = sessionmaker(bind=engine)

def get_order_status(order_id: str) -> dict:
    """Returns order details for a given order_id."""
    with Session() as session:
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if order:
            return {
                "order_id": order.order_id,
                "customer_id": order.customer_id,
                "product_name": order.product_name,
                "order_date": order.order_date,
                "status": order.status,
                "delivery_eta": order.delivery_eta,
                "tracking_number": order.tracking_number
            }
        return None

def get_customer(customer_id: str) -> dict:
    """Returns customer details for a given customer_id."""
    with Session() as session:
        customer = session.query(Customer).filter(Customer.customer_id == customer_id).first()
        if customer:
            return {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "email": customer.email,
                "signup_date": customer.signup_date,
                "loyalty_tier": customer.loyalty_tier
            }
        return None

def get_customer_orders(customer_id: str) -> list:
    """Returns a list of orders for a given customer_id."""
    with Session() as session:
        orders = session.query(Order).filter(Order.customer_id == customer_id).all()
        return [
            {
                "order_id": order.order_id,
                "product_name": order.product_name,
                "status": order.status,
                "delivery_eta": order.delivery_eta
            }
            for order in orders
        ]

def get_ticket(ticket_id: str) -> dict:
    """Returns ticket details for a given ticket_id."""
    with Session() as session:
        ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if ticket:
            return {
                "ticket_id": ticket.ticket_id,
                "customer_id": ticket.customer_id,
                "issue_summary": ticket.issue_summary,
                "sentiment_score": ticket.sentiment_score,
                "escalated": ticket.escalated,
                "created_at": ticket.created_at
            }
        return None

import uuid
from datetime import datetime

def create_ticket(customer_id: str, issue_summary: str) -> dict:
    with Session() as session:
        new_ticket = Ticket(
            ticket_id=str(uuid.uuid4()),
            customer_id=customer_id,
            issue_summary=issue_summary,
            sentiment_score=0.0,
            escalated=False,
            created_at=datetime.utcnow()
        )
        session.add(new_ticket)
        session.commit()
        return {
            "ticket_id": new_ticket.ticket_id,
            "customer_id": new_ticket.customer_id,
            "issue_summary": new_ticket.issue_summary,
            "status": "open"
        }

def update_ticket_status(ticket_id: str, escalated: bool) -> bool:
    with Session() as session:
        ticket = session.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if ticket:
            ticket.escalated = escalated
            session.commit()
            return True
        return False
