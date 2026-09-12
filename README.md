# E-Commerce Database

A genuine multi-table relational database design demonstrating advanced PostgreSQL engineering: foreign keys, check constraints, triggers, stored functions, and views - verified end-to-end with an automated Python test harness. This is a database engineering capstone, going beyond basic CRUD into real data-integrity enforcement at the database layer.

## Schema

    customers ----< orders ----< order_items >---- products
       (1)            (N)  (1)        (N)      (1)

- **customers**: id, name, unique email
- **products**: id, name, price, stock (CHECK: stock >= 0)
- **orders**: id, customer_id (FK), status (CHECK: constrained to valid values)
- **order_items**: id, order_id (FK, ON DELETE CASCADE), product_id (FK), quantity, unit_price

## Advanced Features

### Trigger: Automatic Stock Deduction
When an `order_item` is inserted, a trigger (`trg_deduct_stock`) automatically deducts the ordered quantity from the product's stock - no application-level code needs to remember to do this, and it cannot be bypassed by inserting directly into the database.

### Defense in Depth: Two-Layer Stock Protection
If an order would take stock negative, **two independent safety mechanisms** catch it:
1. The trigger's own `RAISE EXCEPTION` check
2. The `CHECK (stock >= 0)` constraint on the `products` table itself

In testing, the CHECK constraint fires first (since it's evaluated as part of the UPDATE the trigger performs) - meaning even if the trigger's own logic had a bug, the database schema itself still prevents invalid data. This is a deliberate, real demonstration of defense-in-depth data integrity.

### View: Order Summary
`order_summary` is a view that joins orders, customers, and order_items into a single denormalized query - the kind of view a real reporting dashboard or admin panel would query directly, without the application needing to reconstruct the join logic every time.

## Files

| File | Purpose |
|------|---------|
| `01_schema.sql` | Table definitions, constraints, indexes |
| `02_triggers_and_views.sql` | The stock-deduction trigger/function and the order_summary view |
| `03_seed_data.sql` | Sample data for testing and demonstration |
| `test_ecommerce.py` | Automated tests verifying schema, trigger behavior, constraint enforcement, and view correctness |

## Running Locally

    createdb ecommerce
    psql ecommerce -f 01_schema.sql
    psql ecommerce -f 02_triggers_and_views.sql
    psql ecommerce -f 03_seed_data.sql

## Running Tests

    pip install -r requirements.txt
    pytest test_ecommerce.py -v

## Related Repositories

- [python-learning-journey](https://github.com/abdallasaidbigpartner-web/python-learning-journey)
- [typescript-learning-journey](https://github.com/abdallasaidbigpartner-web/typescript-learning-journey)
- [sql-learning-journey](https://github.com/abdallasaidbigpartner-web/sql-learning-journey)
- [ai-study-assistant](https://github.com/abdallasaidbigpartner-web/ai-study-assistant)
- [task-manager-api](https://github.com/abdallasaidbigpartner-web/task-manager-api)
- [study-assistant-frontend](https://github.com/abdallasaidbigpartner-web/study-assistant-frontend)
- [url-shortener-go](https://github.com/abdallasaidbigpartner-web/url-shortener-go)
