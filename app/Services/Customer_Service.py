from app.Repositories.Customer_Repository import *
from datetime import datetime, date

# 新增餐點進購物車
def add_item_to_cart(item_id, item_price, customer_id, redirect_flag):
    restaurant_id = get_restaurant_id_for_item(item_id)
    all_active_orders = check_existing_orders(customer_id)

    existing_order = None
    for order in all_active_orders:
        if order['restaurant_id'] == restaurant_id:
            existing_order = order['order_id']
            break

    if not existing_order:
        existing_order = check_order(customer_id)

    add_one_item_in_cart(item_id, existing_order, item_price)
    return redirect_flag, restaurant_id

# 查看購物車內容
def get_cart_items(customer_id):
    return fetch_cart_item(customer_id)

def remove_item_from_cart(order_id, order_detail_id):
    remove_from_cart(order_id, order_detail_id)

def checkout_order_service(order_id, total_price, pickup_time, payment_method):
    current_date = date.today()
    pickup_time = datetime.strptime(pickup_time, "%H:%M").time()
    pickup_datetime = datetime.combine(current_date, pickup_time)
    formatted_pickup_datetime = pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")

    checkout_order(order_id, total_price, formatted_pickup_datetime, payment_method)

def get_all_orders(customer_id):
    return fetch_all_orders(customer_id)

# 修改訂單狀態回到退回狀態
def return_order_service(order_id, restaurant_id, customer_id):
    all_cart_item = check_existing_orders(customer_id)
    existing_order = False
    for order in all_cart_item:
        if order['restaurant_id'] == restaurant_id:
            existing_order = True
            break
    if existing_order:
        return False
    else:
        return_order(order_id)

def get_customer_profile(customer_id):
    return get_customer_info(customer_id)

def update_customer_profile(customer_id, new_name, new_phone, new_email):
    customer = get_customer_info(customer_id)
    if customer:
        update_customer_info(customer, new_name, new_phone, new_email)
        return True
    return False

def add_note_service(order_id, order_detail_id, note_text):
    return add_note_to_order(order_id, order_detail_id, note_text)

