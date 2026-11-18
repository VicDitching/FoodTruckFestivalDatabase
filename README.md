# Food Truck Festival Database

A portal for festival staff, available as a local web app (`web_app.py`) or a command-line app (`app.py`).
Staff can look up customers, browse trucks and menus, see sales by vendor, register customers,
update contact info, and record orders. Guests can browse food trucks and their menus.
None of it requires writing SQL.

## Requirements

- MySQL Server 8.0+
- Python 3.10+
- `mysql-connector-python` and `flask`

```bash
py -m pip install mysql-connector-python flask
```

## Setup

Run these as **root** in MySQL Workbench (or the `mysql` client), in this order:

1. `setup.sql`: creates the `FoodTruckFestival` schema, constraints, and all sample data
2. `account.sql`: creates the limited application accounts and their grants

## Running

### Web app

```bash
py web_app.py
```

Then open http://127.0.0.1:5000 in a browser. The login page asks for a database account:

| Account | Role | Can use |
|---|---|---|
| `ftf_app` | Admin | Everything: food trucks and menus, customers, place order, premium items, sales report, remove truck |
| `ftf_guest` | Guest | Food trucks and their menus only |

The app connects to MySQL *as* the account that logs in, so MySQL's grants decide what each
user can really do. Guests don't see the admin pages, and the app also refuses them if a guest
types an admin URL directly. `root` is never accepted.

### Command-line app

```bash
py app.py
```

The program asks for the username (default `ftf_app`) and password when it starts.

Neither app stores the password in code, in a file, or in this README.

## Features

| Web page | CLI menu # | Feature | Requirement covered | Function |
|---|---|---|---|---|
| Customers → Search | 1 | Search customers by last name | Search (SELECT + WHERE) | `find_customers_by_last_name` |
| Food Trucks | 4 | List food trucks with their vendors | Combine tables (JOIN) | `get_all_food_trucks` |
| Sales Report | 8 | Vendor sales & order summary | Summary (GROUP BY + COUNT/SUM) | `get_vendor_sales_summary` |
| Premium Items | 6 | Premium menu items (above average price) | Subquery | `get_premium_menu_items` |
| Customers → Register | 2 | Register a new customer | Add (INSERT) | `add_customer` |
| Customers → Update phone | 3 | Update a customer's phone number | Change (UPDATE) | `update_customer_phone` |
| Place Order | 7 | Place an order | Transaction (INSERT CustomerOrder + INSERT OrderItem rows, COMMIT/ROLLBACK) | `place_order` |

Viewing a truck's menu (click a truck, or CLI option 5) is an extra feature.

Each SQL feature has a data function that runs the query and returns rows (used by both apps), plus a
small command-line wrapper (`search_customers`, `vendor_sales_summary`, `high_value_menu_items`,
`update_customer_contact`) that asks for input and prints the result.

**Constraint demo:** Register a customer using a Customer ID that already exists. The PRIMARY KEY rejects it and the app says "That ID is already in use."
**Refused operation demo:** "Remove" on the Food Trucks page (CLI option 9). `ftf_app` has no DELETE permission, so MySQL refuses it (error 1142) and the app says "You do not have permission to delete records."

## Schema changes since the design

- `Location.Zipcode` changed from INT to VARCHAR(10) (zip codes are labels, not numbers, and can have leading zeros).
- `MenuItem.Availability` changed from VARCHAR(45) to BOOLEAN.
- Fixed the `OrderItem` column name from `MenuItem` to `MenuItemID` so it matches its primary and foreign key.

## AI use

- Sample data in `setup.sql` was generated with AI and checked by the team.
- The menu/interface code in `app.py` (menus, input prompts, friendly error messages) was written with AI help.
- The web interface (`web_app.py` and the `templates/` folder: pages, forms, login screen, styling) was written with AI help. AI also split our print-style functions into data functions plus printing wrappers so both apps can share them; the SQL inside them is unchanged.
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

