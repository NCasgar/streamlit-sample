import streamlit as st
import json
import os
import time

# Title for the app
st.title("Fast Food Order System")

# Filepath for storing the orders
orders_file = "orders.json"

# Function to load orders from a file
def load_orders():
    if os.path.exists(orders_file):
        try:
            with open(orders_file, "r") as file:
                data = file.read()
                if not data:
                    return {"PREPARING": [], "READY": []}
                return json.loads(data)
        except json.JSONDecodeError:
            return {"PREPARING": [], "READY": []}
    else:
        return {"PREPARING": [], "READY": []}

# Function to save orders to a file
def save_orders(orders):
    with open(orders_file, "w") as file:
        json.dump(orders, file)

# Load orders from the file
orders = load_orders()

# Main section for Order management
col1, col2, col3 = st.columns([1, 1, 1])

# First column: Add to PREPARING
with col1:
    order_number = st.number_input("ORDER NUMBER", min_value=1, step=1, format="%d")
    if st.button("Add to PREPARING", use_container_width=True):
        if order_number not in orders["PREPARING"] and order_number not in orders["READY"]:
            orders["PREPARING"].append(order_number)
            save_orders(orders)
            message = st.success(f"Order #{order_number} added to 'PREPARING' list.")
            time.sleep(3)
            message.empty()
        elif order_number in orders["READY"]:
            st.error(f"Order #{order_number} is already in the 'READY' list.")
        else:
            st.warning(f"Order #{order_number} is already in the 'PREPARING' list.")

# Second column: Transfer from PREPARING to READY
with col2:
    if orders["PREPARING"]:
        transfer_order_number = st.selectbox("PREPARING", options=orders["PREPARING"], key="transfer_select")
        if st.button("Move to READY", use_container_width=True):
            orders["PREPARING"].remove(transfer_order_number)
            orders["READY"].append(transfer_order_number)
            save_orders(orders)
            message = st.success(f"Order #{transfer_order_number} transferred to 'READY'.")
            time.sleep(3)
            message.empty()

# Third column: Delete from READY
with col3:
    if orders["READY"]:
        delete_order_number = st.selectbox("READY", options=orders["READY"], key="delete_select")
        if st.button("Delete Completed Order", use_container_width=True):
            orders["READY"].remove(delete_order_number)
            save_orders(orders)
            message = st.success(f"Order #{delete_order_number} deleted from 'READY'.")
            time.sleep(3)
            message.empty()

# Row 1 for Select/Update/Search
row1_col1, row1_col2, row1_col3 = st.columns(3)

# Column for Order Number
with row1_col1:
    if orders["PREPARING"]:
        selected_order = st.selectbox("ORDER NUMBER", options=orders["PREPARING"], key="update_select")

# Column for New Order Number
with row1_col2:
    new_order_number = st.number_input("NEW ORDER NUMBER", min_value=1, step=1, format="%d", key="new_order_input")

# Column for Order Number to Search with default null/None
with row1_col3:
    search_number = st.number_input("ORDER NUMBER", min_value=0, step=1, format="%d", key="search_input")

# Row 2 for Update/Search buttons
row2_col1, row2_col2, row2_col3 = st.columns(3)

# Column for Update Order Number button
with row2_col1:
    if st.button("UPDATE Order Number", use_container_width=True):
        if new_order_number not in orders["PREPARING"] and new_order_number not in orders["READY"]:
            orders["PREPARING"].remove(selected_order)
            orders["PREPARING"].append(new_order_number)
            save_orders(orders)
            message = st.success(f"Order #{selected_order} updated to #{new_order_number} in 'PREPARING'.")
            time.sleep(3)
            message.empty()
        elif new_order_number in orders["READY"]:
            st.error(f"Order #{new_order_number} is already in the 'READY' list.")
        else:
            st.warning(f"Order #{new_order_number} is already in the 'PREPARING' list.")

# Column for Sort button
with row2_col2:
    if st.button("SORT Numbers", use_container_width=True):
        orders["PREPARING"].sort()
        orders["READY"].sort()
        save_orders(orders)
        message = st.success("Both PREPARING and READY lists sorted.")
        time.sleep(3)
        message.empty()

# Column for Search Order button
with row2_col3:
    if st.button("SEARCH", use_container_width=True):
        found_in_preparing = search_number in orders["PREPARING"]
        found_in_ready = search_number in orders["READY"]
        if found_in_preparing or found_in_ready:
            message = st.success(f"Order #{search_number} found!")
            time.sleep(3)
            message.empty()
        else:
            message = st.error(f"Order #{search_number} not found in either list.")
            time.sleep(3)
            message.empty()

# Custom CSS for layout and styling
st.markdown("""
    <style>
        .block-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
        .css-1d391kg {
            padding: 0 !important;
        }
        .css-18e3th9 {
            max-width: 100% !important;
        }
        .preparing-box {
            background-color: #ffcccb;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .ready-box {
            background-color: #c8e6c9;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            margin-top: 10px;
        }
        .order-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .order-item {
            background-color: #ffffff;
            padding: 5px 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .highlight {
            background-color: #ff9999 !important;
        }
        button {
            width: 100% !important;
            text-align: center !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Display PREPARING orders with the title "Orders Currently PREPARING"
st.markdown('<div class="preparing-box"><h3>Orders Currently PREPARING</h3>', unsafe_allow_html=True)
preparing_numbers = " ".join([f"<span class='order-item highlight'>{num}</span>" if num == search_number else f"<span class='order-item'>{num}</span>" for num in orders["PREPARING"]])
st.markdown(f"<div class='order-container'>{preparing_numbers}</div></div>", unsafe_allow_html=True)

# Display READY orders with the title "Orders READY for Pickup"
st.markdown('<div class="ready-box"><h3>Orders READY for Pickup</h3>', unsafe_allow_html=True)
ready_numbers = " ".join([f"<span class='order-item highlight'>{num}</span>" if num == search_number else f"<span class='order-item'>{num}</span>" for num in orders["READY"]])
st.markdown(f"<div class='order-container'>{ready_numbers}</div></div>", unsafe_allow_html=True)
