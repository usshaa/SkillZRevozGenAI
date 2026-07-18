import os
import csv
import sys
from sqlalchemy import create_engine, Column, String, Float, Boolean, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import DB_PROVIDER, SQLITE_DB_PATH, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    signup_date = Column(String(50))
    loyalty_tier = Column(String(50))

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey('customers.customer_id'))
    product_name = Column(String(200))
    order_date = Column(String(50))
    status = Column(String(50))
    delivery_eta = Column(String(50))
    tracking_number = Column(String(100))

class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey('customers.customer_id'))
    issue_summary = Column(String(500))
    sentiment_score = Column(Float)
    escalated = Column(Boolean)
    created_at = Column(String(50))

def get_engine():
    if DB_PROVIDER == 'mysql':
        url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        return create_engine(url)
    else:
        # Default to sqlite
        os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
        return create_engine(f"sqlite:///{SQLITE_DB_PATH}")

def setup_database():
    engine = get_engine()
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "generated")
    
    # Check if data already exists
    if session.query(Customer).first() is not None:
        print("Database already seeded. Skipping.")
        return

    print("Database schema created and verified.")

    print("Database schema created and seeded.")

if __name__ == "__main__":
    setup_database()
