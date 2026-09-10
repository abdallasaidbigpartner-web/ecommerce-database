-- Seed data for testing and demonstration

INSERT INTO customers (name, email) VALUES
('Abdalla Said', 'abdalla@example.com'),
('Sara Ahmed', 'sara@example.com');

INSERT INTO products (name, price, stock) VALUES
('Wireless Mouse', 19.99, 50),
('Mechanical Keyboard', 79.99, 20),
('USB-C Hub', 29.99, 5);

INSERT INTO orders (customer_id, status) VALUES
(1, 'pending');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 2, 19.99),
(1, 2, 1, 79.99);
