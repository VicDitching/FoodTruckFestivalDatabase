import sys
import getpass
import mysql.connector
from mysql.connector import Error

def connect_db():
    print("Food Truck Festival Management Portal")
    user = input("Enter DB Usernmae [ftf_app]: ").strip() or "ftf_app"
    password = getpass.getpass("Enter DB password: ")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database="FoodTruckFestival"
        )
        if conn.is_connected():
            print("\nSuccessfully connected to MySQL Database!")
            return conn
    except Error as e:
        print(f"\nConnection Error: {e}")
        sys.exit(1)

def print_table(headers, rows):
    if not rows:
        print("\n[No records found.]")
        return
    print("\n" + " | ".join(headers))
    print("-" * 75)
    for row in rows:
        print(" | ".join(str(val) for val in row))
    print(f"\nTotal Records: {len(rows)}")

#search (SELECT with WHERE)
def search_customers(conn):
    print("\n Search Customer by Last Name")
    term = input("Enter last name (or prefix): ").strip()
    query = """
        SELECT CustomerID, FirstName, LastName, Email, Phone, CreatedAt
        FROM Customer
        WHERE LastName LIKE %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (f"(term)%",))
    rows = cursor.fetchall()
    print_table(["ID", "First Name", "Last Name", "Email", "Phone", "Created At"], rows)
    cursor.close()

#summary (GROUP BY with COUNT and SUM)
def vendor_sales_summary(conn):
    print("\nVendor Sales & Order Summary")
    query = """
        SELECT v.CompanyName, ft.TruckName, COUNT(co.OrderID) AS TotalOrders, COALESCE(SUM(co.TotalAmount), 0.00) AS TotalRevenue
        FROM FoodTruck ft
        JOIN Vendor v ON ft.VendorID = v.VendorID
        LEFT JOIN EventRegistration er ON ft.TruckID = er.TruckID
        LEFT JOIN CustomerOrder co ON er.RegistrationID = co.RegistrationID
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
    print("\nPremium Menu Items (Priced Above Fleet Average)")
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
    print("\nUpdate Customer Phone Number")
    cid = input("Enter Customer ID: ").strip()
    new_phone = input("Enter New Phone Number: ").strip()

    query = "UPDATE Customer SET Phone = %s WHERE CustomerID = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query, (new_phone, cid))
        if cursor.rowcount == 0:
           print("\n[Notice]: No customer found with that ID. No chnages made.")
        else:
            conn.commit()
            print(f"\nSuccessfully updated phone number for Customer ID {cid}.")
    except Error as e:
        conn.rollback()
        print(f"\n[Error]: {e}")
    finally:
        cursor.close()

# -------------------- READ FOOD TRUCKS --------------------

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
    cursor = connection.cursor(dictionary=True)
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
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (truck_id,))
        return cursor.fetchall()
    finally:
        cursor.close()


# -------------------- ADD --------------------

def add_food_truck(conn, truck_id, truck_name, license_plate, vendor_id):
    """Insert a food truck, VendorID needs to be an existing vendor"""
    query = """
        INSERT INTO FoodTruck (TruckID, TruckName, LicensePlate, VendorID)
        VALUES (%s, %s, %s, %s)
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, (truck_id, truck_name, license_plate, vendor_id))
        connection.commit()
    except Exception:
        connection.rollback()
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
    cursor = connection.cursor()
    try:
        cursor.execute(query, (customer_id, first_name, last_name, email, phone))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


# -------------------- EDIT FOOD TRUCKS --------------------

def update_food_truck(conn, truck_id, truck_name, license_plate, vendor_id):
    """Update all editable fields for the truck with this TruckID."""
    query = """
        UPDATE FoodTruck
        SET TruckName = %s, LicensePlate = %s, VendorID = %s
        WHERE TruckID = %s
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, (truck_name, license_plate, vendor_id, truck_id))
        connection.commit()
        return cursor.rowcount
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


def update_food_truck_name(conn, truck_id, new_name):
    """Change only a truck's name."""
    query = "UPDATE FoodTruck SET TruckName = %s WHERE TruckID = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (new_name, truck_id))
        connection.commit()
        return cursor.rowcount
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


def update_food_truck_license_plate(conn, truck_id, new_license_plate):
    """Change only a truck's license plate."""
    query = "UPDATE FoodTruck SET LicensePlate = %s WHERE TruckID = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (new_license_plate, truck_id))
        connection.commit()
        return cursor.rowcount
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


def update_food_truck_vendor(conn, truck_id, new_vendor_id):
    """Assign a truck to a different existing vendor."""
    query = "UPDATE FoodTruck SET VendorID = %s WHERE TruckID = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (new_vendor_id, truck_id))
        connection.commit()
        return cursor.rowcount
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


# -------------------- DELETE FOOD TRUCK --------------------

def delete_food_truck(conn, truck_id):
    """Delete a truck by ID."""
    query = "DELETE FROM FoodTruck WHERE TruckID = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (truck_id,))
        connection.commit()
        return cursor.rowcount
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        
