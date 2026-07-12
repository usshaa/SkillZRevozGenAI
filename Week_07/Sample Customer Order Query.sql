-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS customer_support_db;
USE customer_support_db;

-- 2. Create the Orders Table
-- This matches the exact schema your AI Agent is expecting in its prompt.
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_email VARCHAR(255) NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    refund_amount DECIMAL(10, 2) DEFAULT 0.00,
    notes TEXT
);

-- 3. Insert Sample Data
-- This gives your AI Agent realistic scenarios to practice on (Full refunds, partial refunds, active orders).
INSERT INTO orders (order_id, customer_email, order_date, status, total_amount, refund_amount, notes) 
VALUES 
    (9980, 'vip-customer@domain.com', '2026-07-01', 'Delivered', 150.00, 0.00, 'Customer requested replacement.'),
    (9981, 'sarah.j@example.com', '2026-07-05', 'Processing', 85.50, 0.00, 'Awaiting fulfillment.'),
    (9982, 'vip-customer@domain.com', '2026-07-08', 'Refund Pending', 200.00, 200.00, 'Full refund approved for order 9982.'),
    (9983, 'mike.smith@example.com', '2026-07-10', 'Refund Processed', 350.00, 175.00, '50% Prorated refund applied.'),
    (9984, 'vip-customer@domain.com', '2026-07-11', 'Shipped', 45.99, 0.00, 'In transit.');
    
-- Insert 2 new orders for Usha (usshaa48)
INSERT INTO orders (order_id, customer_email, order_date, status, total_amount, refund_amount, notes) 
VALUES 
    (10001, 'usshaa48@gmail.com', '2026-07-12', 'Delivered', 120.50, 0.00, 'First order. Standard delivery.'),
    (10002, 'usshaa48@gmail.com', '2026-07-12', 'Refund Pending', 75.00, 75.00, 'Customer requested cancellation before shipping.');
    
-- Insert the specific records for usshaa48 using integer IDs
INSERT INTO orders (order_id, customer_email, order_date, status, total_amount, refund_amount, notes) 
VALUES 
    (99887, 'usshaa48@gmail.com', '2026-07-13', 'Shipped', 299.99, 0.00, 'Upgraded to express shipping.'),
    (99888, 'usshaa48@gmail.com', '2026-07-14', 'Processing', 45.00, 0.00, 'Pending warehouse scan.');

-- Insert 5 additional sample orders for testing
INSERT INTO orders (order_id, customer_email, order_date, status, total_amount, refund_amount, notes)
VALUES
    (99889, 'alex.w@example.com', '2026-07-10', 'Delivered', 120.00, 0.00, 'Left at front door.'),
    (99890, 'maria.c@domain.com', '2026-07-11', 'Refund Pending', 89.50, 89.50, 'Defective item returned.'),
    (99891, 'tech.buyer@startup.io', '2026-07-12', 'Shipped', 1050.00, 0.00, 'Signature required on delivery.'),
    (99892, 'l.chang@example.com', '2026-07-12', 'Processing', 15.99, 0.00, 'Standard ground shipping.'),
    (99893, 'vip-customer@domain.com', '2026-07-13', 'Refund Processed', 500.00, 50.00, '10% partial refund for late delivery.');    