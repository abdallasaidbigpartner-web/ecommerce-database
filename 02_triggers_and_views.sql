-- Advanced SQL: Triggers, Functions, and Views
-- Demonstrates: automatic stock deduction on order, and a
-- denormalized view for common reporting queries.

-- Function + trigger: automatically deduct stock when an order item is inserted
CREATE OR REPLACE FUNCTION deduct_stock() RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET stock = stock - NEW.quantity
    WHERE id = NEW.product_id;

    IF (SELECT stock FROM products WHERE id = NEW.product_id) < 0 THEN
        RAISE EXCEPTION 'Insufficient stock for product %', NEW.product_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_deduct_stock
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION deduct_stock();

-- View: a denormalized summary of orders with customer name and total value
CREATE OR REPLACE VIEW order_summary AS
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    o.status,
    o.created_at,
    SUM(oi.quantity * oi.unit_price) AS total_value
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id, c.name, o.status, o.created_at;
