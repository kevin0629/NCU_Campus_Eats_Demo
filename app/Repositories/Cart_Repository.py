from app.Repositories.Campus_Eats_Repository import *
from app.Repositories import get_session
from sqlalchemy import text
from datetime import datetime, timedelta
import json

# 4.1 新增餐點進購物車
def add_one_item_in_cart(db_session, item_id, order_id, item_price):
    existing_order_detail = db_session.query(OrderDetail).filter_by(
        order_id=order_id,
        item_id=item_id
    ).first()
    if existing_order_detail:
        existing_order_detail.quantity += 1
        db_session.commit()
    else:
        new_order_detail = OrderDetail(
            order_id=order_id,
            item_id=item_id,
            item_price=item_price,
            quantity=1
        )
        db_session.add(new_order_detail)
        db_session.commit()

# 4.1 新增訂單資料 (還在購物車時的暫存資料)
def check_order(db_session, customer_id):
    current_time = datetime.now() # 記錄下訂單的時間
    new_order = OrderTable(
        order_status=0,
        total_amount=0,
        payment_status=0,
        customer_id=customer_id,
        order_time=current_time,
        order_pick_up_time = current_time # 暫存取餐時間為當下下單時間
    )
    db_session.add(new_order)
    db_session.commit()
    db_session.refresh(new_order)
    return new_order.order_id if new_order else None

# 4.1 查詢該產品所屬的店家
def get_restaurant_id_for_item(db_session, item_id):
    query = text("""
        SELECT restaurant_id
        FROM menu_item
        WHERE item_id = :item_id;
    """)
    result = db_session.execute(query, {"item_id": item_id}).scalar()
    return result if result else None

# 4.1 + 5.4 查當前用戶擁有的所有購物車
def check_existing_orders(db_session, customer_id):
    # 查找所有屬於該使用者且狀態為零的訂單
    query = text("""
        SELECT order_id
        FROM order_table
        WHERE customer_id = :customer_id AND order_status = 0;
    """)
    orders = db_session.execute(query, {"customer_id": customer_id}).fetchall()

    # 根據訂單的 id 去訂單細項表格隨便抓取一格內容商品，並在通過該商品之編號去menu表格裡查詢所屬店家
    restaurant_ids = []
    for order in orders:
        order_id = order[0]
        # 從訂單細項表中隨便抓取一筆內容商品
        with get_session() as db_session:
            item_query = text("""
                SELECT item_id
                FROM order_detail
                WHERE order_id = :order_id
                LIMIT 1;
            """)
            item_id = db_session.execute(item_query, {"order_id": order_id}).scalar()

        if item_id:
            # 通過該商品的編號去 menu_item 表格查詢所屬店家
            restaurant_id = get_restaurant_id_for_item(db_session, item_id)
            if restaurant_id:
                restaurant_ids.append({"order_id": order_id, "restaurant_id": restaurant_id})

    return restaurant_ids

# 4.3 + 5.5刪除整筆購物車
def delete_order_from_cart(db_session, order_id):
    order = db_session.query(OrderTable).filter_by(order_id=order_id).first()
    if order:
        order.order_status = 5 # 訂單狀態設置為 "尚未送出"
        db_session.commit()
        return True

# 4.2 抓取目前所擁有的所有購物車內容
def fetch_cart_item(db_session, customer_id):
    query = text("""
        SELECT order_table.order_id, order_table.order_note, order_detail.order_detail_id, order_detail.item_id, 
            menu_item.item_name, menu_item.price, order_detail.quantity, order_detail.item_note, 
            menu_item.restaurant_id, restaurant.restaurant_name, restaurant.business_hours
        FROM order_table
        JOIN order_detail ON order_table.order_id = order_detail.order_id
        JOIN menu_item ON order_detail.item_id = menu_item.item_id
        JOIN restaurant ON restaurant.restaurant_id = menu_item.restaurant_id
        WHERE order_table.order_status = 0 AND order_table.customer_id = :customer_id;
    """)
    result = db_session.execute(query, {"customer_id": customer_id}).fetchall()

    grouped_cart_items = {}
    for row in result:
        order_id = row[0]
        order_note = row[1]
        order_detail_id = row[2]
        item_id = row[3]
        item_name = row[4]
        item_price = row[5]
        item_quantity = row[6]
        item_note = row[7]
        restaurant_id = row[8]
        restaurant_name = row[9]
        restaurant_business_hours= row[10]

        # 計算單筆商品的小計
        item_total_price = item_price * item_quantity

        # 生成可以取餐的時間(目前是設定如果店接下來有開的話可以選的範圍就是兩個小時，然後十五分鐘為間隔)
        available_times = get_available_times(restaurant_business_hours)

        if restaurant_id not in grouped_cart_items:
            grouped_cart_items[restaurant_id] = {
                "restaurant_name": restaurant_name,
                "order_id": order_id,
                "order_note": order_note,
                "items": [],
                "total_price": 0,
                "available_times": available_times
            }

        grouped_cart_items[restaurant_id]["items"].append({
            "order_detail_id": order_detail_id,
            "order_id": order_id,
            "item_id": item_id,
            "item_name": item_name,
            "price": item_price,
            "quantity": item_quantity,
            "item_note": item_note,
            "item_total_price": item_total_price
        })

        grouped_cart_items[restaurant_id]["total_price"] += item_total_price

    return grouped_cart_items

# 4.3 移除一個商品
def remove_from_cart(db_session, order_id, order_detail_id):
    existing_order_detail = db_session.query(OrderDetail).filter_by(
        order_detail_id=order_detail_id,
        order_id=order_id
    ).first()

    if existing_order_detail:
        if existing_order_detail.quantity > 1:
            # 如果數量大於 1，則減少一個商品數量
            existing_order_detail.quantity -= 1
            db_session.commit()
        else:
            # 如果數量為 1，則刪除該項目
            db_session.delete(existing_order_detail)
            db_session.commit()
            update_order_status_if_empty(db_session, order_id)

# 4.3 檢查該訂單是否還有其他訂單細項，若無則將訂單狀態改為 5 (已退回)
def update_order_status_if_empty(db_session, order_id):
    remaining_items = db_session.query(OrderDetail).filter_by(
        order_id=order_id,
    ).count()

    if remaining_items == 0:
        existing_order = db_session.query(OrderTable).filter_by(order_id=order_id).first()
        if existing_order:
            existing_order.order_status = 5
            db_session.commit()

# 生成可以取餐的時間(目前是設定如果店接下來有開的話可以選的範圍就是兩個小時，然後十五分鐘為間隔)
def get_available_times(business_hours):
    now = datetime.now()
    weekday_map = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    today_weekday = weekday_map[now.weekday()]
    business_hours_dict = {}
    for day_info in business_hours.split(", "):
        day, hours = day_info.split(": ")
        business_hours_dict[day] = hours
    today_hours = business_hours_dict.get(today_weekday)
    if today_hours is None or today_hours == 'Closed':
        return []
    open_time_str, close_time_str = today_hours.split("~")
    open_time = datetime.strptime(open_time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    close_time = datetime.strptime(close_time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    if now >= close_time:
        return []
    earliest_pickup_time = now + timedelta(minutes=15)
    minute = earliest_pickup_time.minute
    if minute < 15:
        adjusted_minute = 15
    elif minute < 30:
        adjusted_minute = 30
    elif minute < 45:
        adjusted_minute = 45
    else:
        adjusted_minute = 0
        earliest_pickup_time += timedelta(hours=1)
    earliest_pickup_time = earliest_pickup_time.replace(minute=adjusted_minute, second=0, microsecond=0)
    available_times = []
    current_time = max(earliest_pickup_time, open_time)
    end_time = min(now + timedelta(hours=2), close_time)
    while current_time < end_time:
        if current_time.minute in [0, 15, 30, 45]:
            available_times.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=15)
    available_times_json = json.dumps(available_times)
    return available_times_json 

