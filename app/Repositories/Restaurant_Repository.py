from app.Repositories.Campus_Eats_Repository import *
from app.Repositories import get_session
from sqlalchemy import desc

# 餐廳相關==============================================================================================================

# 2.1 取得餐廳資訊
def get_restaurant_info(db_session, restaurant_id):
    result = db_session.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()
    print("result---", result.address)
    return result

# 2.2 更新餐廳資訊
def update_restaurant_info(db_session, restaurant_info, restaurant_name, phone, address, business_hours, manager, manager_email, image_path):
    restaurant_info.restaurant_name = restaurant_name
    restaurant_info.phone = phone
    restaurant_info.address = address
    restaurant_info.business_hours = business_hours
    restaurant_info.manager = manager
    restaurant_info.manager_email = manager_email
    restaurant_info.icon = image_path
    db_session.commit()

# 餐點相關==============================================================================================================

# 2.3 確認餐點是否已經存在過
def item_exists(db_session, restaurant_id, item_name):
    return db_session.query(MenuItem).filter_by(item_name=item_name, restaurant_id=restaurant_id).first() is not None

# 2.3 取得最後一筆餐點
def get_last_item(db_session):
    return db_session.query(MenuItem).order_by(desc(MenuItem.item_id)).first()

# 2.3 新增餐點
def add_item(db_session, restaurant_id, item_name, price, description, status, image_path):
    with get_session() as db_session:
        new_item = MenuItem(item_name=item_name, price=price, description=description, status=status, item_image=image_path, restaurant_id=restaurant_id)
        db_session.add(new_item)
        db_session.commit()

# 2.4 取得餐點資訊
def get_item_info(db_session, item_id):
    return db_session.query(MenuItem).filter_by(item_id=item_id).first()

# 2.4 店家查看各餐點資訊頁面
def get_menu_item_by_id(db_session, item_id):
    menu_item = db_session.query(MenuItem).filter_by(item_id=item_id).first()
    if menu_item:
        return {
            'item_id': menu_item.item_id,
            'item_name': menu_item.item_name,
            'price': menu_item.price,
            'description': menu_item.description,
            'status': menu_item.status,
            'item_image': menu_item.item_image
        }
    return None

# 2.4 更新餐點資訊
def update_item_info(db_session, item_info, item_name, price, description, status, image_path):
    item_info.item_name = item_name
    item_info.price = price
    item_info.description = description
    item_info.status = status
    item_info.item_image = image_path
    db_session.commit()

# 2.5 刪除餐點
def delete_item(db_session, item_id):
    item_info = db_session.query(MenuItem).filter_by(item_id=item_id).first()
    db_session.delete(item_info)
    db_session.commit()



# 訂單相關==============================================================================================================

# 2.6 取得待處理訂單
def get_pending_orders(db_session, restaurant_id):
    result = (
        db_session.query(
            OrderTable,
            OrderDetail.order_detail_id, OrderDetail.item_id, OrderDetail.item_note,
            OrderDetail.quantity, OrderDetail.item_price,
            MenuItem.item_name
        )
        .join(OrderTable, OrderDetail.order_id == OrderTable.order_id)
        .join(MenuItem, OrderDetail.item_id == MenuItem.item_id)
        .join(Restaurant, MenuItem.restaurant_id == Restaurant.restaurant_id)
        .filter(MenuItem.restaurant_id == restaurant_id, OrderTable.order_status.between(1,4), OrderTable.payment_status == 0)
        .order_by(desc(OrderTable.order_time))
        .all()
    )
    return result

# 2.7 取得歷史訂單
def get_history_orders(db_session, restaurant_id):
    result = (
        db_session.query(
            OrderTable.order_id, OrderTable.total_amount, OrderTable.order_time, OrderTable.payment_method,
            OrderTable.order_note, OrderTable.order_pick_up_time, OrderTable.customer_id,
            OrderDetail.order_detail_id, OrderDetail.item_id, OrderDetail.item_note,
            OrderDetail.quantity, OrderDetail.item_price,
            MenuItem.item_name
        )
        .join(OrderTable, OrderDetail.order_id == OrderTable.order_id)
        .join(MenuItem, OrderDetail.item_id == MenuItem.item_id)
        .join(Restaurant, MenuItem.restaurant_id == Restaurant.restaurant_id)
        .filter(MenuItem.restaurant_id == restaurant_id, OrderTable.payment_status == 1)
        .all()
    )
    return result

# 2.8 更新訂單狀態
def update_order_status(db_session, order_id, order_status):
    order_info = db_session.query(OrderTable).filter_by(order_id=order_id).first()
    order_info.order_status = order_status
    db_session.commit()

# 2.9 更新付款狀態
def update_payment_status(db_session, order_id, payment_status):
    order_info = db_session.query(OrderTable).filter_by(order_id=order_id).first()
    order_info.payment_status = payment_status
    db_session.commit()

