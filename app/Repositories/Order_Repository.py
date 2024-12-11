from app.Repositories.Campus_Eats_Repository import *
from sqlalchemy import text
from datetime import datetime, timedelta
import json

# 5.1 + 5.2 抓取所有狀態非 0 和 5 的屬於指定客戶的訂單
def fetch_all_orders(db_session, customer_id):
    query = text("""
        SELECT order_table.order_id, order_table.customer_id, order_table.order_status, order_table.order_time, order_table.total_amount,
                order_table.payment_status, order_table.payment_method,
                order_detail.order_detail_id, order_detail.item_id, menu_item.item_name, menu_item.price, order_detail.quantity,
                menu_item.restaurant_id, restaurant.restaurant_name
        FROM order_table
        JOIN order_detail ON order_table.order_id = order_detail.order_id
        JOIN menu_item ON order_detail.item_id = menu_item.item_id
        JOIN restaurant ON restaurant.restaurant_id = menu_item.restaurant_id
        WHERE order_table.order_status NOT IN (0, 5) AND order_table.customer_id = :customer_id;
    """)
    result = db_session.execute(query, {"customer_id": customer_id}).fetchall()

    grouped_orders = {}
    for row in result:
        order_id = row[0]
        customer_id = row[1]
        order_status = row[2]
        order_time = row[3]
        total_amount = row[4]
        payment_status = row[5]
        payment_method = row[6]
        restaurant_id = row[12]
        restaurant_name = row[13]
        
        # 將訂單資訊加入字典中
        if order_id not in grouped_orders:
            grouped_orders[order_id] = {
                "customer_id": customer_id,
                "order_status": order_status,
                "order_time": order_time,
                "total_amount": total_amount,
                "payment_status": "已付款" if payment_status == 1 else "未付款",
                "payment_method": "現金" if payment_method == 1 else "信用卡" if payment_method == 2 else "尚未付款",
                "restaurants": {}
            }

        # 將餐廳資訊加入訂單
        if restaurant_id not in grouped_orders[order_id]["restaurants"]:
            grouped_orders[order_id]["restaurants"][restaurant_id] = {
                "restaurant_name": restaurant_name,
                "restaurant_id": restaurant_id,
                "items": []
            }

        # 將餐點資訊加入餐廳
        grouped_orders[order_id]["restaurants"][restaurant_id]["items"].append({
            "order_detail_id": row[7],
            "item_id": row[8],
            "item_name": row[9],
            "price": row[10],
            "quantity": row[11]
        })

    return grouped_orders

# 5.3 送出訂單
def checkout_order(db_session, order_id, total_price, formatted_pickup_datetime, payment_method):
    order = db_session.query(OrderTable).filter_by(order_id=order_id).first()

    if order:
        order.order_status = 1 # 設定狀態為 1 表示已送出
        order.total_amount = total_price # 更新總金額
        order.order_pick_up_time = formatted_pickup_datetime # 更新成訂單送出時間
        order.payment_method = payment_method # 更新付款方式
        db_session.commit()

# 5.3.2新增訂單備註
def add_note_to_order(db_session, order_id, order_detail_id, note_text):
    if order_detail_id:
        order_detail = db_session.query(OrderDetail).filter_by(order_detail_id=order_detail_id, order_id=order_id).first()
        if order_detail:
            order_detail.item_note = note_text
        else:
            return False
    else:
        order = db_session.query(OrderTable).filter_by(order_id=order_id).first()
        if order:
            order.order_note = note_text
        else:
            return False
    db_session.commit()
    return True
    
# 5.4 修改訂單狀態回到退回狀態
def return_order(db_session, order_id):
    order = db_session.query(OrderTable).filter_by(order_id=order_id).first()
    if order:
        order.order_status = 0
        order.total_amount = 0
        db_session.commit()


