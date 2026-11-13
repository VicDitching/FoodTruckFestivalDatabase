import sys
import getpass
import datetime
from decimal import Decimal
import mysql.connector
from mysql.connector import Error
from mysql.connector.constants import ClientFlag
from mysql.connector import errorcode

def connect_db():
    print_heading("Food Truck Festival Management Portal")
    user = input("Enter DB Username [ftf_app]: ").strip() or "ftf_app"
    password = getpass.getpass("Enter DB password: ")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database="FoodTruckFestival",
            # Make rowcount report rows *matched*, not just rows changed, so an
            # UPDATE that sets a value to what it already was isn't treated as
            # "no record found".
            client_flags=[ClientFlag.FOUND_ROWS],
        )
        print("\nSuccessfully connected to MySQL Database!")
        return conn
    except Error as e:
        if e.errno == 1045:
            print("\nLogin failed: wrong username or password.")
        elif e.errno == 1049:
            print("\nThe FoodTruckFestival database does not exist. Run setup.sql first.")
        elif e.errno == 1044:
            print("\nThis account is not allowed to use the FoodTruckFestival database.")
        elif e.errno in (2003, 2005):
            print("\nCould not reach the MySQL server. Make sure it is running.")
        else:
            print("\nCould not connect to the database.")
        sys.exit(1)

# -------------------- DISPLAY HELPERS (interface code, AI-assisted) --------------------

def print_heading(title):
    print("\n" + title)
    print("=" * len(title))


def _format_cell(header, value):
    if value is None:
        return "-"
    if header == "Available":
        return "Yes" if value else "No"
    if isinstance(value, (Decimal, float)):
        return f"{value:,.2f}"
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, datetime.date):
        return value.isoformat()
    return str(value)


def print_table(headers, rows, max_width=40):
    """Print rows as a lined-up table. Numbers are right-aligned."""
    if not rows:
        print("\n  No records found.")
        return

    cells = [[_format_cell(h, v) for h, v in zip(headers, row)] for row in rows]
    cells = [[c if len(c) <= max_width else c[:max_width - 3] + "..." for c in row]
             for row in cells]
    widths = [max(len(h), *(len(row[i]) for row in cells)) for i, h in enumerate(headers)]
    numeric = [all(isinstance(row[i], (int, float, Decimal)) or row[i] is None
                   for row in rows) and headers[i] != "Available"
               for i in range(len(headers))]

    def line(values):
        return "  " + " | ".join(
            v.rjust(w) if num else v.ljust(w)
            for v, w, num in zip(values, widths, numeric))

    print()
    print(line(headers))
    print("  " + "-+-".join("-" * w for w in widths))
    for row in cells:
        print(line(row))
    print(f"\n  {len(rows)} record{'s' if len(rows) != 1 else ''} found.")

def friendly_error(err):
    """Translate an expected MySQL error into a message for the user."""
    code = getattr(err, "errno", None)
    msg = str(err)

    if code == errorcode.ER_DUP_ENTRY:                      # 1062
        if "orderitem.primary" in msg.lower():
            return "The same menu item was entered twice in one order. Enter each item once with its total quantity."
        if "PRIMARY" in msg:
            return "That ID is already in use. Please choose a different ID."
        if "Email" in msg or "email" in msg:
            return "This email is already registered."
        if "LicensePlate" in msg:
            return "That license plate is already registered to another truck."
        return "That value is already in use and must be unique."
    if code == errorcode.ER_NO_REFERENCED_ROW_2:            # 1452
        return ("One of the IDs you entered does not exist "
                "(for example the customer, booth registration, or menu item).")
    if code == errorcode.ER_ROW_IS_REFERENCED_2:            # 1451
        return "This record is still used by other records and cannot be removed."
    if code in (errorcode.ER_TABLEACCESS_DENIED_ERROR,      # 1142
                errorcode.ER_COLUMNACCESS_DENIED_ERROR,     # 1143
                errorcode.ER_DBACCESS_DENIED_ERROR):        # 1044
        # MySQL's message starts with the refused command, e.g. "DELETE command denied..."
        verbs = {"DELETE": "delete", "INSERT": "add", "UPDATE": "change",
                 "DROP": "drop", "CREATE": "create", "ALTER": "alter"}
        verb = verbs.get(msg.split(":")[-1].strip().split(" ")[0].upper())
        if verb:
            return f"You do not have permission to {verb} records."
        return "You do not have permission to perform this action."
    if code == 3819:                                        # CHECK constraint
        return "One of the values is not allowed (it breaks a data rule)."
    if code == errorcode.ER_BAD_NULL_ERROR:                 # 1048
        return "A required field was left empty."
    if code == errorcode.ER_DATA_TOO_LONG:                  # 1406
        return "One of the values you typed is too long."
    if code == errorcode.ER_WARN_DATA_OUT_OF_RANGE:         # 1264
        return "One of the numbers is too large (for example the quantity or order total)."
    return "The database could not complete that request. Please try again."


#search (SELECT with WHERE)
def search_customers(conn):
    print_heading("Search Customers by Last Name")
    term = input("Last name (or first few letters): ").strip()
    query = """
        SELECT CustomerID, FirstName, LastName, Email, Phone, CreatedAt
        FROM Customer
        WHERE LastName LIKE %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (f"{term}%",))
    rows = cursor.fetchall()
    print_table(["ID", "First Name", "Last Name", "Email", "Phone", "Created At"], rows)
    cursor.close()

#summary (GROUP BY with COUNT and SUM)
def vendor_sales_summary(conn):
    print_heading("Vendor Sales & Order Summary (completed orders)")
    query = """
        SELECT v.CompanyName, ft.TruckName, COUNT(co.OrderID) AS TotalOrders, COALESCE(SUM(co.TotalAmount), 0.00) AS TotalRevenue
        FROM FoodTruck ft
        JOIN Vendor v ON ft.VendorID = v.VendorID
        LEFT JOIN EventRegistration er ON ft.TruckID = er.TruckID 
        LEFT JOIN CustomerOrder co ON er.RegistrationID = co.RegistrationID AND co.orderstatus = 'completed'
        GROUP BY v.CompanyName, ft.TruckName
        ORDER BY TotalRevenue DESC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print_table(["Vendor", "Truck Name", "Orders Placed", "Total Sales ($)"], rows)
    cursor.close()

#subquery (above-average menu items)
def high_value_menu_items(conn):
    print_heading("Premium Menu Items (priced above the average item)")
    query = """
        SELECT MenuItemID, ItemName, Price, DietaryFlags, Availability
        FROM MenuItem
        WHERE Price > (SELECT AVG(Price) FROM MenuItem)
        ORDER BY Price DESC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print_table(["Item ID", "Item Name", "Price ($)", "Dietary Flags", "Available"], rows)
    cursor.close()

#change (UPDATE)
def update_customer_contact(conn):
    print_heading("Update a Customer's Phone Number")
    cid = input("Customer ID: ").strip()
    if not cid.isdigit():
        print("\nCustomer ID must be a whole number. No changes made.")
        return
    new_phone = input("New phone number: ").strip()
    if not new_phone:
        print("\nPhone number cannot be empty. No changes made.")
        return

    query = "UPDATE Customer SET Phone = %s WHERE CustomerID = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query, (new_phone, cid))
        if cursor.rowcount == 0:
            print("\nNo customer found with that ID. No changes made.")
        else:
            conn.commit()
            print(f"\nSuccessfully updated phone number for Customer ID {cid}.")
    except Error:
        conn.rollback()
        raise  # app.py shows a friendly message instead of the raw MySQL error
    finally:
        cursor.close()

# Read Food Trucks

def get_all_food_trucks(conn):
    """Return every food truck and its info"""
    query = """
        SELECT ft.TruckID, ft.TruckName, ft.LicensePlate,
               ft.VendorID, v.CompanyName
        FROM FoodTruck AS ft
        LEFT JOIN Vendor AS v ON ft.VendorID = v.VendorID
        ORDER BY ft.TruckName
    """
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()


def get_food_truck(conn, truck_id):
    """Return a single food truck """
    query = "SELECT * FROM FoodTruck WHERE TruckID = %s"
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, (truck_id,))
        return cursor.fetchone()
    finally:
        cursor.close()


def get_food_truck_menu(conn, truck_id):
    """Return all menu items from a truck"""
    query = """
        SELECT MenuItemID, ItemName, Description, Price,
               DietaryFlags, Availability
        FROM MenuItem
        WHERE TruckID = %s
        ORDER BY ItemName
    """
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, (truck_id,))
        return cursor.fetchall()
    finally:
        cursor.close()


# Add stuff

def add_food_truck(conn, truck_id, truck_name, license_plate, vendor_id):
    """Insert a food truck, VendorID needs to be an existing vendor"""
    query = """
        INSERT INTO FoodTruck (TruckID, TruckName, LicensePlate, VendorID)
        VALUES (%s, %s, %s, %s)
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query, (truck_id, truck_name, license_plate, vendor_id))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


def add_customer(conn, customer_id, first_name, last_name, email, phone):
    """Insert a new customer setting CreatedAt to the current database time."""
    query = """
        INSERT INTO Customer
            (CustomerID, FirstName, LastName, Email, Phone, CreatedAt)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query, (customer_id, first_name, last_name, email, phone))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


# Edit Food Trucks

def update_food_truck(conn, truck_id, truck_name, license_plate, vendor_id):
    """Update all editable fields for the truck with this TruckID."""
    query = """
        UPDATE FoodTruck
        SET TruckName = %s, LicensePlate = %s, VendorID = %s
        WHERE TruckID = %s
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query, (truck_name, license_plate, vendor_id, truck_id))
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


def update_food_truck_name(conn, truck_id, new_name):
    """Change only a truck's name."""
    query = "UPDATE FoodTruck SET TruckName = %s WHERE TruckID = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query, (new_name, truck_id))
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


def update_food_truck_license_plate(conn, truck_id, new_license_plate):
    """Change only a truck's license plate."""
    query = "UPDATE FoodTruck SET LicensePlate = %s WHERE TruckID = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query, (new_license_plate, truck_id))
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


def update_food_truck_vendor(conn, truck_id, new_vendor_id):
    """Assign a truck to a different existing vendor."""
    query = "UPDATE FoodTruck SET VendorID = %s WHERE TruckID = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query, (new_vendor_id, truck_id))
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


# Place ORders

#transaction 
def place_order(conn, order_id, customer_id, registration_id, payment_method, items):
    cursor= conn.cursor()
    try:
        total_amount = Decimal('0.00')
        item_data = []

        #verifies items and calculates the total amount
        for menu_item_id, quantity in items:
            price_query = "SELECT Price FROM MenuItem WHERE MenuItemID = %s"
            cursor.execute(price_query, (menu_item_id,))
            row = cursor.fetchone()
            if not row:
                print(f"\n[Error] Menu Item ID {menu_item_id} does not exist.")
                conn.rollback()
                return False
            unit_price= row[0]
            total_amount += unit_price * quantity
            item_data.append((menu_item_id, quantity, unit_price))

        #inserts the main order record into CustomerOrder
        order_query = """
            INSERT INTO CustomerOrder(OrderID, OrderDateTime, OrderStatus, TotalAmount, PaymentMethod, CustomerID, RegistrationID)
            VALUES (%s, NOW(), 'Completed', %s, %s, %s, %s)
        """
        cursor.execute(order_query, (order_id, total_amount, payment_method, customer_id, registration_id))

        #inserts all items into OrderItem
        item_query = """
            INSERT INTO OrderItem(OrderID, MenuItemID, Quantity, UnitPriceAtSale)
            VALUES(%s, %s, %s, %s)
        """
        for menu_item_id, quantity, unit_price in item_data:
            cursor.execute(item_query, (order_id, menu_item_id, quantity, unit_price))

        #commit transaction if all steps succeed
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        print(f"\n[Error] {friendly_error(e)}")
        return False
    finally:
        cursor.close()


# Delete Foodie

def delete_food_truck(conn, truck_id):
    """Delete a truck by ID."""
    query = "DELETE FROM FoodTruck WHERE TruckID = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query, (truck_id,))
        conn.commit()
        return cursor.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        
