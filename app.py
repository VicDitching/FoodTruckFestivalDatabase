"""
Food Truck Festival Management Portal - menu / interface layer.

This file only handles the menu, user input, and turning MySQL errors into
friendly messages. All SQL lives in food_truck_functions.py.

(Interface code written with AI help, allowed by Section 5 of the assignment.)
"""

import mysql.connector

import food_truck_functions as ftf


# ------------------------------------------------------------------ helpers

def ask_int(prompt):
    """Keep asking until the user types a whole number."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a whole number.")


def ask_text(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value or None
        print("  This field cannot be empty.")


friendly_error = ftf.friendly_error  # shared with food_truck_functions


def run_feature(func):
    """Run one menu feature; never let an expected error reach the user raw."""
    try:
        func()
    except NotImplementedError:
        print("\n[Not available yet] This feature has not been implemented.")
    except mysql.connector.Error as err:
        print(f"\n[Error] {friendly_error(err)}")


# ------------------------------------------------------------ menu actions
# Each action collects input, then calls a function in food_truck_functions.

def action_search_customers(conn):
    ftf.search_customers(conn)


def action_list_trucks(conn):
    ftf.print_heading("Food Trucks and Their Vendors")
    rows = ftf.get_all_food_trucks(conn)
    ftf.print_table(
        ["Truck ID", "Truck Name", "Plate", "Vendor ID", "Vendor"],
        [(r["TruckID"], r["TruckName"], r["LicensePlate"],
          r["VendorID"], r["CompanyName"]) for r in rows],
    )


def action_truck_menu(conn):
    ftf.print_heading("View a Truck's Menu")
    truck_id = ask_int("Truck ID (option 4 lists them): ")
    truck = ftf.get_food_truck(conn, truck_id)
    if truck is None:
        print("\nNo food truck found with that ID.")
        return
    print(f"\nMenu for {truck['TruckName']}:")
    rows = ftf.get_food_truck_menu(conn, truck_id)
    ftf.print_table(
        ["Item ID", "Item", "Price ($)", "Dietary Flags", "Available"],
        [(r["MenuItemID"], r["ItemName"], r["Price"], r["DietaryFlags"],
          r["Availability"]) for r in rows],
    )


def action_sales_summary(conn):
    ftf.vendor_sales_summary(conn)


def action_premium_items(conn):
    ftf.high_value_menu_items(conn)


def action_add_customer(conn):
    ftf.print_heading("Register a New Customer")
    customer_id = ask_int("Customer ID: ")
    first = ask_text("First name: ")
    last = ask_text("Last name: ")
    email = ask_text("Email: ")
    phone = ask_text("Phone (optional): ", required=False)
    ftf.add_customer(conn, customer_id, first, last, email, phone)
    print(f"\nCustomer {first} {last} was added with ID {customer_id}.")


def action_update_phone(conn):
    ftf.update_customer_contact(conn)


def action_place_order(conn):
    ftf.print_heading("Place an Order")
    order_id = ask_int("New Order ID: ")
    customer_id = ask_int("Customer ID: ")
    registration_id = ask_int("Booth Registration ID (truck at an event): ")
    payment = ask_text("Payment method (Card / Cash / Mobile Pay): ")

    items = []
    print("Enter menu items. Leave the item ID empty when done.")
    while True:
        raw = input("  Menu Item ID: ").strip()
        if not raw:
            break
        if not raw.isdigit():
            print("  Please enter a whole number.")
            continue
        qty = ask_int("  Quantity: ")
        if qty <= 0:
            print("  Quantity must be at least 1.")
            continue
        items.append((int(raw), qty))

    if not items:
        print("\nAn order needs at least one item. Nothing was saved.")
        return

    ok = ftf.place_order(conn, order_id, customer_id, registration_id,
                         payment, items)
    if ok:
        print(f"\nOrder {order_id} was saved.")
    else:
        print("\nThe order could not be completed. No changes were saved.")


def action_delete_truck(conn):
    ftf.print_heading("Remove a Food Truck")
    truck_id = ask_int("Truck ID to remove: ")
    count = ftf.delete_food_truck(conn, truck_id)
    if count == 0:
        print("\nNo food truck found with that ID.")
    else:
        print(f"\nFood truck {truck_id} was removed.")


# (section title, [(menu label, action), ...]) -- numbering runs across sections
MENU_SECTIONS = [
    ("Customers", [
        ("Search customers by last name",            action_search_customers),
        ("Register a new customer",                  action_add_customer),
        ("Update a customer's phone number",         action_update_phone),
    ]),
    ("Trucks & Menus", [
        ("List food trucks with their vendors",      action_list_trucks),
        ("View a truck's menu",                      action_truck_menu),
        ("Premium menu items (above average price)", action_premium_items),
    ]),
    ("Orders & Reports", [
        ("Place an order",                           action_place_order),
        ("Vendor sales & order summary",             action_sales_summary),
    ]),
    ("Admin", [
        ("Remove a food truck",                      action_delete_truck),
    ]),
]
MENU = [item for _, items in MENU_SECTIONS for item in items]


def show_menu():
    print("\n" + "=" * 48)
    print("        FOOD TRUCK FESTIVAL PORTAL")
    print("=" * 48)
    number = 1
    for title, items in MENU_SECTIONS:
        print(f"\n {title}")
        for label, _ in items:
            print(f"   {number}. {label}")
            number += 1
    print("\n   0. Exit")


def pause():
    input("\nPress Enter to return to the menu...")


def main():
    conn = ftf.connect_db()
    try:
        while True:
            show_menu()
            choice = input("\nChoose an option: ").strip()

            if choice == "0":
                print("Goodbye!")
                break
            if not choice.isdigit() or not 1 <= int(choice) <= len(MENU):
                print("Please choose a number from the menu.")
                continue

            _, action = MENU[int(choice) - 1]
            # Start each menu action with a fresh view of the data. Without
            # this, MySQL keeps showing the snapshot from the first SELECT, so
            # changes made elsewhere (e.g. in Workbench) never appear here.
            # Every feature that writes data already commits on its own, so
            # nothing is pending at this point.
            conn.commit()
            run_feature(lambda: action(conn))
            pause()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
