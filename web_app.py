"""
Food Truck Festival Portal - local web interface.

Run:  py web_app.py   then open http://127.0.0.1:5000

The login page asks for a MySQL account. The app connects AS that account,
so MySQL's own permissions decide what each user can really do:
  - ftf_app   -> admin pages (same features as the command-line app)
  - ftf_guest -> guest pages (food trucks and their menus only)
root is never accepted. Passwords are never stored in code or on disk;
they are only used to open the database connection.

All SQL lives in food_truck_functions.py. This file is interface code
(written with AI help, allowed by Section 5 of the assignment).
"""

import contextlib
import io
import os
import secrets
from decimal import Decimal
from functools import wraps

import mysql.connector
from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)
from mysql.connector.constants import ClientFlag

import food_truck_functions as ftf

ADMIN_ACCOUNTS = {"ftf_app"}
GUEST_ACCOUNTS = {"ftf_guest"}

app = Flask(__name__)
app.secret_key = os.urandom(32)          # new key each run: old logins expire

# Open database connections, keyed by a random token kept in the session
# cookie. The password itself is never put in the cookie.
_connections = {}


# ------------------------------------------------------------------ helpers

def make_table(headers, rows, link=None):
    """Format query rows for the table template (same formatting as the CLI)."""
    numeric = [bool(rows) and headers[i] != "Available" and
               all(isinstance(r[i], (int, float, Decimal)) or r[i] is None for r in rows)
               for i in range(len(headers))]
    body = []
    for r in rows:
        body.append({
            "cells": [ftf._format_cell(h, v) for h, v in zip(headers, r)],
            "link": link(r) if link else None,
            "raw": r,
        })
    return {"headers": headers, "rows": body, "numeric": numeric}


def parse_int(value, field):
    try:
        return int((value or "").strip())
    except ValueError:
        raise ValueError(f"{field} must be a whole number.")


def friendly(err):
    return ftf.friendly_error(err)


def login_required(role=None):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if g.get("conn") is None:
                return redirect(url_for("login", next=request.path))
            if role == "admin" and session.get("role") != "admin":
                return render_template("forbidden.html"), 403
            return view(*args, **kwargs)
        return wrapper
    return decorator


@app.before_request
def load_connection():
    token = session.get("token")
    conn = _connections.get(token) if token else None
    if conn is not None:
        try:
            conn.ping(reconnect=False)
            # Fresh view of the data for every page (see app.py main loop).
            conn.commit()
        except mysql.connector.Error:
            _connections.pop(token, None)
            session.clear()
            flash("The database connection was lost. Please log in again.", "error")
            conn = None
    g.conn = conn


@app.context_processor
def inject_user():
    return {"user": session.get("user"), "role": session.get("role")}


# ------------------------------------------------------------------- login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if user == "root":
            flash("This app never connects as root. Use ftf_app (admin) or ftf_guest (guest).", "error")
            return render_template("login.html", username=user)
        if user not in ADMIN_ACCOUNTS | GUEST_ACCOUNTS:
            flash("Unknown account. Use ftf_app (admin) or ftf_guest (guest).", "error")
            return render_template("login.html", username=user)

        try:
            conn = mysql.connector.connect(
                host="localhost", user=user, password=password,
                database="FoodTruckFestival",
                client_flags=[ClientFlag.FOUND_ROWS],
            )
        except mysql.connector.Error as e:
            messages = {
                1045: "Login failed: wrong username or password.",
                1049: "The FoodTruckFestival database does not exist. Run setup.sql first.",
                1044: "This account is not allowed to use the FoodTruckFestival database.",
                2003: "Could not reach the MySQL server. Make sure it is running.",
            }
            flash(messages.get(e.errno, "Could not connect to the database."), "error")
            return render_template("login.html", username=user)

        old = _connections.pop(session.get("token"), None)
        if old is not None:
            old.close()
        token = secrets.token_hex(16)
        _connections[token] = conn
        session.clear()
        session.update(token=token, user=user,
                       role="admin" if user in ADMIN_ACCOUNTS else "guest")
        return redirect(request.args.get("next") or url_for("trucks"))

    return render_template("login.html", username="")


@app.route("/logout", methods=["POST"])
def logout():
    conn = _connections.pop(session.get("token"), None)
    if conn is not None:
        conn.close()
    session.clear()
    flash("You have been logged out.", "ok")
    return redirect(url_for("login"))


# ---------------------------------------------------- guest + admin pages

@app.route("/")
def home():
    return redirect(url_for("trucks"))


@app.route("/trucks")
@login_required()
def trucks():
    try:
        rows = ftf.get_all_food_trucks(g.conn)
    except mysql.connector.Error as e:
        flash(friendly(e), "error")
        rows = []
    data = [(r["TruckID"], r["TruckName"], r["CompanyName"], r["LicensePlate"]) for r in rows]
    table = make_table(["Truck ID", "Truck Name", "Vendor", "Plate"], data,
                       link=lambda r: url_for("truck_menu", truck_id=r[0]))
    return render_template("trucks.html", table=table)


@app.route("/trucks/<int:truck_id>")
@login_required()
def truck_menu(truck_id):
    try:
        truck = ftf.get_food_truck(g.conn, truck_id)
        if truck is None:
            flash("No food truck found with that ID.", "error")
            return redirect(url_for("trucks"))
        rows = ftf.get_food_truck_menu(g.conn, truck_id)
    except mysql.connector.Error as e:
        flash(friendly(e), "error")
        return redirect(url_for("trucks"))
    data = [(r["MenuItemID"], r["ItemName"], r["Description"], r["Price"],
             r["DietaryFlags"], r["Availability"]) for r in rows]
    table = make_table(["Item ID", "Item", "Description", "Price ($)", "Dietary Flags", "Available"], data)
    return render_template("truck_menu.html", truck=truck, table=table)


# -------------------------------------------------------------- admin pages

@app.route("/trucks/<int:truck_id>/delete", methods=["POST"])
@login_required("admin")
def delete_truck(truck_id):
    try:
        count = ftf.delete_food_truck(g.conn, truck_id)
        if count == 0:
            flash("No food truck found with that ID.", "error")
        else:
            flash(f"Food truck {truck_id} was removed.", "ok")
    except mysql.connector.Error as e:
        flash(friendly(e), "error")
    return redirect(url_for("trucks"))


@app.route("/customers")
@login_required("admin")
def customers():
    term = request.args.get("q", "").strip()
    table = None
    if "q" in request.args:
        try:
            rows = ftf.find_customers_by_last_name(g.conn, term)
            table = make_table(["ID", "First Name", "Last Name", "Email", "Phone", "Created At"], rows)
        except mysql.connector.Error as e:
            flash(friendly(e), "error")
    return render_template("customers.html", table=table, term=term)


@app.route("/customers/add", methods=["POST"])
@login_required("admin")
def add_customer():
    f = request.form
    try:
        cid = parse_int(f.get("customer_id"), "Customer ID")
        first, last, email = (f.get(k, "").strip() for k in ("first", "last", "email"))
        if not (first and last and email):
            raise ValueError("First name, last name and email are required.")
        phone = f.get("phone", "").strip() or None
        ftf.add_customer(g.conn, cid, first, last, email, phone)
        flash(f"Customer {first} {last} was added with ID {cid}.", "ok")
        return redirect(url_for("customers", q=last))
    except ValueError as e:
        flash(str(e), "error")
    except mysql.connector.Error as e:
        flash(friendly(e), "error")
    return redirect(url_for("customers"))


@app.route("/customers/phone", methods=["POST"])
@login_required("admin")
def update_phone():
    f = request.form
    try:
        cid = parse_int(f.get("customer_id"), "Customer ID")
        phone = f.get("phone", "").strip()
        if not phone:
            raise ValueError("Phone number cannot be empty.")
        if ftf.update_customer_phone(g.conn, cid, phone) == 0:
            flash("No customer found with that ID. No changes made.", "error")
        else:
            flash(f"Updated phone number for Customer ID {cid}.", "ok")
    except ValueError as e:
        flash(str(e), "error")
    except mysql.connector.Error as e:
        flash(friendly(e), "error")
    return redirect(url_for("customers"))


@app.route("/menu/premium")
@login_required("admin")
def premium():
    try:
        rows = ftf.get_premium_menu_items(g.conn)
    except mysql.connector.Error as e:
        flash(friendly(e), "error")
        rows = []
    table = make_table(["Item ID", "Item Name", "Price ($)", "Dietary Flags", "Available"], rows)
    return render_template("table_page.html", title="Premium Menu Items", color="sun",
                           subtitle="The fancy stuff: items priced above the average menu item.", table=table)


@app.route("/reports/sales")
@login_required("admin")
def sales():
    try:
        rows = ftf.get_vendor_sales_summary(g.conn)
    except mysql.connector.Error as e:
        flash(friendly(e), "error")
        rows = []
    table = make_table(["Vendor", "Truck Name", "Orders Placed", "Total Sales ($)"], rows)
    return render_template("table_page.html", title="Vendor Sales Summary", color="grape",
                           subtitle="Completed orders and revenue for each truck.", table=table)


@app.route("/orders/new", methods=["GET", "POST"])
@login_required("admin")
def new_order():
    form = request.form if request.method == "POST" else {}
    if request.method == "POST":
        try:
            order_id = parse_int(form.get("order_id"), "Order ID")
            customer_id = parse_int(form.get("customer_id"), "Customer ID")
            registration_id = parse_int(form.get("registration_id"), "Booth Registration ID")
            payment = form.get("payment", "").strip()
            if not payment:
                raise ValueError("Choose a payment method.")

            items = []
            for item_raw, qty_raw in zip(request.form.getlist("item_id"),
                                         request.form.getlist("qty")):
                if not item_raw.strip():
                    continue
                item = parse_int(item_raw, "Menu Item ID")
                qty = parse_int(qty_raw or "1", "Quantity")
                if qty <= 0:
                    raise ValueError("Quantity must be at least 1.")
                items.append((item, qty))
            if not items:
                raise ValueError("An order needs at least one item. Nothing was saved.")

            # place_order (the team's transaction) prints its own error
            # message; capture it so it can be shown on the page.
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                ok = ftf.place_order(g.conn, order_id, customer_id,
                                     registration_id, payment, items)
            if ok:
                flash(f"Order {order_id} was saved.", "ok")
                return redirect(url_for("new_order"))
            reason = captured.getvalue().strip().removeprefix("[Error]").strip()
            flash((reason + " " if reason else "") +
                  "The order was cancelled and no changes were saved.", "error")
        except ValueError as e:
            flash(str(e), "error")
        except mysql.connector.Error as e:
            flash(friendly(e), "error")

    # Keep what the user typed when the order fails; start with 3 empty rows.
    item_rows = [(i, q) for i, q in zip(request.form.getlist("item_id"),
                                        request.form.getlist("qty")) if i.strip()]
    item_rows += [("", "1")] * max(1, 3 - len(item_rows))
    return render_template("order.html", form=form, item_rows=item_rows)


if __name__ == "__main__":
    print("Food Truck Festival Portal running at http://127.0.0.1:5000  (Ctrl+C to stop)")
    # threaded=False: one request at a time, so a connection is never shared
    # between two requests at once.
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=False)
