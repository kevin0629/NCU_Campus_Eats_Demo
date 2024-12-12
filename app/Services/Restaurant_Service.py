import os
from app.Repositories.Restaurant_Repository import *

# 餐廳相關==============================================================================================================

# 2.1 取得餐廳資訊Service
def get_store_info_service(db_session, restaurant_id):
    # 取得餐廳資訊
    store_info = get_restaurant_info(db_session, restaurant_id)

    # 初始化一個包含所有天的字典，值為空列表
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    business_hours = {day: [] for day in days_of_week}

    # 解析營業時間字串
    raw_business_hours = store_info.business_hours
    if raw_business_hours:
        # 分割每天的營業時間條目
        for entry in raw_business_hours.split(", "):
            day, times = entry.split(": ")
            # 將每一天的時段列表拆解後放入對應的 key
            business_hours[day] = times.split("、")

    store_data = {
        "restaurant_id": restaurant_id,
        "restaurant_name": store_info.restaurant_name,
        "phone": store_info.phone,
        "address": store_info.address,
        "business_hours": business_hours,
        "manager": store_info.manager,
        "manager_email": store_info.manager_email,
        "icon": store_info.icon
    }
    return store_data

# 2.2 更新餐廳資訊Service
def update_store_info_service(db_session, restaurant_id, restaurant_name, phone, address, manager, manager_email, icon, hours):
    # 取得餐廳資訊
    restaurant_info = get_restaurant_info(db_session, restaurant_id)

    if icon and icon.filename:
        # 處理圖片
        filename, file_extension = os.path.splitext(icon.filename)
        filename = str(restaurant_info.restaurant_id) + file_extension
        image_path = os.path.join('images/restaurants', filename)  # 儲存相對路徑
        image_path = image_path.replace("\\", "/")
        os.makedirs(os.path.dirname(os.path.join('./app/static', image_path)), exist_ok=True)  # 確保目錄存在
        icon.save(os.path.join('./app/static', image_path))  # 儲存圖片
    else:
        image_path = restaurant_info.icon  # 若無圖片則設為之前的圖片

    # 僅包含有時段的日子
    business_hours = ", ".join(f"{day}: {'、'.join(times)}" for day, times in hours.items() if times)

    # 更新餐廳資訊
    update_restaurant_info(db_session, restaurant_info, restaurant_name, phone, address, business_hours, manager, manager_email, image_path)
    return {'success': '餐廳資訊更新成功', 'icon': image_path}

# 餐點相關==============================================================================================================

# 2.3 新增餐點Service
def add_menu_item_service(db_session, restaurant_id, item_name, price, description, status, item_image):
    # 確認餐點是否已經存在過
    if item_exists(db_session, restaurant_id, item_name):
        return {'error': '餐點已存在'}

    if item_image and item_image.filename:
        last_item = get_last_item(db_session)
        item_id = 0 if last_item is None else last_item.item_id

        # 處理圖片
        filename, file_extension = os.path.splitext(item_image.filename)
        filename = str(item_id + 1) + file_extension
        image_path = os.path.join('images/menus', filename)  # 儲存相對路徑
        image_path = image_path.replace("\\", "/")  # 防止 Windows 路徑問題
        os.makedirs(os.path.dirname(os.path.join('./app/static', image_path)), exist_ok=True)  # 確保目錄存在
        item_image.save(os.path.join('./app/static', image_path))  # 儲存圖片
    else:
        image_path = 'images/menus/menu.png'  # 若無圖片則設為 None

    # 新增餐點
    add_item(db_session, restaurant_id, item_name, price, description, status, image_path)
    return {'success': '餐點新增成功'}

# 2.4 店家查看各餐點資訊頁面
def get_menu_item_by_id_service(db_session, item_id):
    return get_menu_item_by_id(db_session, item_id)

# 2.4 更新餐點Service
def update_menu_item_service(db_session, item_id, item_name, price, description, status, item_image):
    # 取得餐點資訊
    item_info = get_item_info(db_session, item_id)

    if item_image and item_image.filename:
        # 處理圖片
        filename, file_extension = os.path.splitext(item_image.filename)
        filename = str(item_info.item_id) + file_extension
        image_path = os.path.join('images/menus', filename)  # 儲存相對路徑
        image_path = image_path.replace("\\", "/")  # 防止 Windows 路徑問題
        os.makedirs(os.path.dirname(os.path.join('./app/static', image_path)), exist_ok=True)  # 確保目錄存在
        item_image.save(os.path.join('./app/static', image_path))  # 儲存圖片
    else:
        image_path = item_info.item_image  # 若無圖片則設為上一張圖片

    # 更新餐點資訊
    update_item_info(db_session, item_info, item_name, price, description, status, image_path)
    return {'success': '餐點資訊更新成功'}

# 2.5 刪除餐點Service
def delete_menu_item_service(db_session, item_id):
    delete_item(db_session, item_id)
    return {'success': '餐點刪除成功'}

# 訂單相關==============================================================================================================

# 2.6 取得待處理訂單Service
def get_pending_orders_service(db_session, restaurant_id):
    result = get_pending_orders(db_session, restaurant_id)
    order_process = {}
    for row in result:
        order_id = row[0].order_id
        total_amount = row[0].total_amount
        order_status = row[0].order_status
        order_time = row[0].order_time.strftime('%Y-%m-%d %H:%M:%S')
        payment_method = row[0].payment_method
        payment_status = row[0].payment_status
        order_note = row[0].order_note
        order_pick_up_time = row[0].order_pick_up_time.strftime('%Y-%m-%d %H:%M:%S')
        customer_id = row[0].customer_id
        order_detail_id = row[1]
        item_id = row[2]
        item_note = row[3]
        quantity = row[4]
        price = row[5]
        item_name = row[6]

        if not order_note:
            order_note = "無"
        
        if not item_note:
            item_note = "無"
        
        # 將訂單資訊加入字典中
        if order_id not in order_process:
            order_process[order_id] = {
                "customer_id": customer_id,
                "order_status": order_status,
                "order_time": order_time,
                "total_amount": total_amount,
                "order_note": order_note,
                "order_pick_up_time": order_pick_up_time,
                "payment_status": "已付款" if payment_status == 1 else "未付款",
                "payment_method": "現金" if payment_method == 1 else "信用卡" if payment_method == 2 else "尚未付款",

                "order_details": {}
            }
            
        # 將訂單詳細資訊加入訂單
        if order_detail_id not in order_process[order_id]["order_details"]:
            order_process[order_id]["order_details"][order_detail_id] = {
                "item_id": item_id,
                "item_name": item_name,
                "price": price,
                "quantity": quantity,
                "item_note": item_note
            }
    return order_process

# 2.7 取得歷史訂單Service
def get_history_orders_service(db_session, restaurant_id):
    result = get_history_orders(db_session, restaurant_id)
    history_order = {}
    for row in result:
        order_id = row[0]
        total_amount = row[1]
        order_time = row[2].strftime('%Y-%m-%d %H:%M:%S')
        payment_method = row[3]
        order_note = row[4]
        order_pick_up_time = row[5].strftime('%Y-%m-%d %H:%M:%S')  # 將 datetime 轉換為字符串
        customer_id = row[6]
        order_detail_id = row[7]
        item_id = row[8]
        item_note = row[9]
        quantity = row[10]
        price = row[11]
        item_name = row[12]

        if not order_note:
            order_note = "無"
        
        if not item_note:
            item_note = "無"
        
        # 將訂單資訊加入字典中
        if order_id not in history_order:
            history_order[order_id] = {
                "customer_id": customer_id,
                "order_time": order_time,
                "total_amount": total_amount,
                "order_note": order_note,
                "order_pick_up_time": order_pick_up_time,
                "payment_method": "現金" if payment_method == 1 else "信用卡" if payment_method == 2 else "尚未付款",

                "order_details": {}
            }
            
        # 將訂單詳細資訊加入訂單
        if order_detail_id not in history_order[order_id]["order_details"]:
            history_order[order_id]["order_details"][order_detail_id] = {
                "item_id": item_id,
                "item_name": item_name,
                "price": price,
                "quantity": quantity,
                "item_note": item_note
            }
    return history_order

# 2.8 更新訂單狀態Service
def update_order_status_service(db_session, order_id, order_status):
    update_order_status(db_session, order_id, order_status)

# 2.9 更新付款狀態Service
def update_payment_status_service(db_session, order_id, payment_status):
    update_payment_status(db_session, order_id, payment_status)



