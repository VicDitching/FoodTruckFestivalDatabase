


# -------------------- READ FOOD TRUCKS --------------------

def get_all_food_trucks(connection):
    """Return every food truck and its info"""
    query = """
        SELECT ft.TruckID, ft.TruckName, ft.LicensePlate,
               ft.VendorID, v.CompanyName
        FROM FoodTruck AS ft
        LEFT JOIN Vendor AS v ON ft.VendorID = v.VendorID
        ORDER BY ft.TruckName
    """
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()


def get_food_truck(connection, truck_id):
    """Return a single food truck """
    query = "SELECT * FROM FoodTruck WHERE TruckID = %s"
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (truck_id,))
        return cursor.fetchone()
    finally:
        cursor.close()


def get_food_truck_menu(connection, truck_id):
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

def add_food_truck(connection, truck_id, truck_name, license_plate, vendor_id):
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


def add_customer(connection, customer_id, first_name, last_name, email, phone):
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

def update_food_truck(connection, truck_id, truck_name, license_plate, vendor_id):
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


def update_food_truck_name(connection, truck_id, new_name):
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


def update_food_truck_license_plate(connection, truck_id, new_license_plate):
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


def update_food_truck_vendor(connection, truck_id, new_vendor_id):
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

def delete_food_truck(connection, truck_id):
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
