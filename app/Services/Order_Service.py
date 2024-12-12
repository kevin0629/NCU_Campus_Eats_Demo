from app.Repositories.Order_Repository import *
from app.Repositories.Cart_Repository import *
from datetime import datetime, timedelta, timezone

taiwan_tz = timezone(timedelta(hours=+8))

# 5.1 + 5.2抓取所有狀態非 0 和 5 的屬於指定客戶的訂單
def get_all_orders_service(db_session, customer_id):
    return fetch_all_orders(db_session, customer_id)

# 5.3 送出訂單Service
def checkout_order_service(db_session, order_id, total_price, pickup_time, payment_method):
    now = datetime.now(taiwan_tz)
    current_date = now.date()
    pickup_time = datetime.strptime(pickup_time, "%H:%M").time()
    pickup_datetime = datetime.combine(current_date, pickup_time)
    formatted_pickup_datetime = pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")

    checkout_order(db_session, order_id, total_price, formatted_pickup_datetime, payment_method)

# 5.3.2 新增訂單備註
def add_note_service(db_session, order_id, order_detail_id, note_text):
    return add_note_to_order(db_session, order_id, order_detail_id, note_text)

# 5.4 修改訂單狀態回到退回狀態Service
def return_order_service(db_session, order_id, restaurant_id, customer_id):
    all_cart_item = check_existing_orders(db_session, customer_id)
    existing_order = False
    for order in all_cart_item:
        if order['restaurant_id'] == restaurant_id:
            existing_order = True
            return True

    if not existing_order:
        return_order(db_session, order_id)
        return False
        


