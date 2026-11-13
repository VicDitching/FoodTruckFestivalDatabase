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

| # | Menu option | Requirement covered | Function |
|---|-------------|---------------------|----------|
| 1 | Search customers by last name | Search (SELECT + WHERE) | `search_customers` |
| 2 | TODO | Combine tables (JOIN) | TODO |
| 3 | Vendor sales & order summary | Summary (GROUP BY) | `vendor_sales_summary` |
| 4 | Premium menu items | Subquery | `high_value_menu_items` |
| 5 | Register a new customer | Add (INSERT) | `add_customer` |
| 6 | Update a customer's phone number | Change (UPDATE) | `update_customer_contact` |
| 7 | Place an order | Transaction | `place_order` |

**Constraint demo:** TODO (e.g. registering a customer with an ID or email that is already used)
**Refused operation demo:** "Remove a food truck". `ftf_app` has no DELETE permission, so MySQL refuses it (error 1142).

## Schema changes since the design

- TODO (e.g. `Zipcode` changed from INT to VARCHAR(10), `MenuItem.Availability` changed to BOOLEAN, any UNIQUE/CHECK added)

## AI use

- Sample data in `setup.sql` was generated with AI and checked by the team.
- The menu/interface code in `app.py` (menus, input prompts, friendly error messages) was written with AI help.
- AI was used to debug the interface/connection code, and to review our SQL and point out bugs. The SQL fixes themselves were written by the team.
- All required SQL, the parameterized queries, the account grants, and the transaction logic were written by the team.

## Team

| Member | Responsibilities |
|--------|------------------|
| Jay | | - created the GUI of the database - contributed in creating the database and functions |
| Victoria | | - created the sql for both customer and vendor account - contributed in creating the database and functions |

