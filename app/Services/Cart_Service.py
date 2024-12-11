from app.Repositories.Cart_Repository import *
from datetime import datetime, date


# 4.1 新增餐點進購物車Service
def add_item_to_cart(db_session, item_id, item_price, customer_id):
    restaurant_id = get_restaurant_id_for_item(db_session, item_id)
    all_active_orders = check_existing_orders(db_session, customer_id)

    existing_order = None
    for order in all_active_orders:
        if order['restaurant_id'] == restaurant_id:
            existing_order = order['order_id']
            break

    if not existing_order:
        existing_order = check_order(db_session, customer_id)

    add_one_item_in_cart(db_session, item_id, existing_order, item_price)
    return restaurant_id

# 4.2 查看購物車內容
def get_cart_items(db_session, customer_id):
    return fetch_cart_item(db_session, customer_id)

# 4.3 移除購物車一個商品
def remove_item_from_cart(db_session, order_id, order_detail_id):
    remove_from_cart(db_session, order_id, order_detail_id)

