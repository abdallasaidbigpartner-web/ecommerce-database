"""
Automated tests for the E-Commerce Database capstone.

Verifies the schema, trigger-based stock deduction, the safety
constraint preventing negative stock, and the order_summary view -
using Python + psycopg2 as a test harness against a real PostgreSQL
database, the same professional pattern used in sql-learning-journey.
"""

import subprocess
import psycopg2
import pytest


@pytest.fixture(scope="module", autouse=True)
def reset_database():
    """Reset the ecommerce database to a known state before running tests."""
    conn = psycopg2.connect(dbname="ecommerce")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS order_items, orders, products, customers CASCADE;")
    conn.commit()
    cursor.close()
    conn.close()

    subprocess.run(["psql", "ecommerce", "-f", "01_schema.sql"], check=True, capture_output=True)
    subprocess.run(["psql", "ecommerce", "-f", "02_triggers_and_views.sql"], check=True, capture_output=True)
    subprocess.run(["psql", "ecommerce", "-f", "03_seed_data.sql"], check=True, capture_output=True)

    yield


def get_connection():
    return psycopg2.connect(dbname="ecommerce")


def test_schema_created_correctly():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers;")
    customer_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM products;")
    product_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert customer_count == 2
    assert product_count == 3


def test_trigger_deducted_stock_correctly():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stock FROM products WHERE name = 'Wireless Mouse';")
    stock = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    # Seed data ordered 2 units from a starting stock of 50
    assert stock == 48, f"Expected 48 after trigger deduction, got {stock}"


def test_stock_cannot_go_negative():
    conn = get_connection()
    cursor = conn.cursor()

    with pytest.raises(psycopg2.errors.CheckViolation):
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (1, 3, 100, 29.99);"
        )

    conn.rollback()
    cursor.close()
    conn.close()


def test_order_summary_view_computes_correct_total():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT total_value FROM order_summary WHERE order_id = 1;")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    # 2 * 19.99 + 1 * 79.99 = 119.97
    assert float(total) == 119.97


def test_foreign_key_prevents_orphaned_order():
    conn = get_connection()
    cursor = conn.cursor()

    with pytest.raises(psycopg2.errors.ForeignKeyViolation):
        cursor.execute("INSERT INTO orders (customer_id, status) VALUES (9999, 'pending');")

    conn.rollback()
    cursor.close()
    conn.close()
