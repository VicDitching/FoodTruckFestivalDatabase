# Food Truck Festival Database

A command-line portal for festival staff. They can look up customers, browse trucks and menus,
see sales by vendor, register customers, update contact info, and record orders.
None of it requires writing SQL.

## Requirements

- MySQL Server 8.0+
- Python 3.10+
- `mysql-connector-python`

```bash
py -m pip install mysql-connector-python
```

## Setup

Run these as **root** in MySQL Workbench (or the `mysql` client), in this order:

1. `setup.sql`: creates the `FoodTruckFestival` schema, constraints, and all sample data
2. `account.sql`: creates the limited `ftf_app` account and its grants

## Running

```bash
py app.py
```

The program asks for the username (default `ftf_app`) and password when it starts.
The password is never stored in the code or in this README.

## Features

| Menu # | Menu option | Requirement covered | Function |
|---|-------------|---------------------|----------|
| 1 | Search customers by last name | Search (SELECT + WHERE) | `search_customers` |
| 4 | List food trucks with their vendors | Combine tables (JOIN) | `get_all_food_trucks` |
| 8 | Vendor sales & order summary | Summary (GROUP BY + COUNT/SUM) | `vendor_sales_summary` |
| 6 | Premium menu items (above average price) | Subquery | `high_value_menu_items` |
| 2 | Register a new customer | Add (INSERT) | `add_customer` |
| 3 | Update a customer's phone number | Change (UPDATE) | `update_customer_contact` |
| 7 | Place an order | Transaction (INSERT CustomerOrder + INSERT OrderItem rows, COMMIT/ROLLBACK) | `place_order` |

Option 5 (View a truck's menu) is an extra feature.

**Constraint demo:** Register a customer (option 2) using a Customer ID that already exists. The PRIMARY KEY rejects it and the app says "That ID is already in use."
**Refused operation demo:** "Remove a food truck" (option 9). `ftf_app` has no DELETE permission, so MySQL refuses it (error 1142) and the app says "You do not have permission to delete records."

## Schema changes since the design

- `Location.Zipcode` changed from INT to VARCHAR(10) (zip codes are labels, not numbers, and can have leading zeros).
- `MenuItem.Availability` changed from VARCHAR(45) to BOOLEAN.
- Fixed the `OrderItem` column name from `MenuItem` to `MenuItemID` so it matches its primary and foreign key.

## AI use

- Sample data in `setup.sql` was generated with AI and checked by the team.
- The menu/interface code in `app.py` (menus, input prompts, friendly error messages) was written with AI help.
- AI was used to debug the interface/connection code, and to review our SQL and point out bugs. The SQL fixes themselves were written by the team.
- AI was used to help format the README
- All required SQL, the parameterized queries, the account grants, and the transaction logic were written by the team.

## Team
Member: Jay 
- created the GUI of the database
- contributed in creating the database and functions
  
Member: Victoria
- created the sql for both customer and vendor account
- contributed in creating the database and functions

