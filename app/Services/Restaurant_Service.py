import os
from app.Repositories.Restaurant_Repository import *

def add_menu_item(restaurant_id, item_name, price, description, status, item_image):
    if item_exists(restaurant_id, item_name):
        return {'error': '餐點已存在'}

    if item_image and item_image.filename:
        last_item = get_last_item()
        item_id = 0 if last_item is None else last_item.item_id

        # 處理圖片
        filename, file_extension = os.path.splitext(item_image.filename)
        filename = str(item_id + 1) + file_extension
        image_path = os.path.join('images/menus', filename)  # 儲存相對路徑
        image_path = image_path.replace("\\", "/")  # 防止 Windows 路徑問題
        os.makedirs(os.path.dirname(os.path.join('./static', image_path)), exist_ok=True)  # 確保目錄存在
        item_image.save(os.path.join('./static', image_path))  # 儲存圖片
    else:
        image_path = 'images/menus/menu.png'  # 若無圖片則設為 None

    add_item(restaurant_id, item_name, price, description, status, image_path)
    return {'success': '餐點新增成功'}

def update_store_info(restaurant_id, restaurant_name, phone, address, manager, manager_email, icon, hours):
    restaurant_info = get_restaurant_info(restaurant_id)
    if icon and icon.filename:
        # 處理圖片
        filename, file_extension = os.path.splitext(icon.filename)
        filename = str(restaurant_info.restaurant_id) + file_extension
        image_path = os.path.join('images/restaurants', filename)  # 儲存相對路徑
        image_path = image_path.replace("\\", "/")
        os.makedirs(os.path.dirname(os.path.join('./static', image_path)), exist_ok=True)  # 確保目錄存在
        icon.save(os.path.join('./static', image_path))  # 儲存圖片
    else:
        image_path = restaurant_info.icon  # 若無圖片則設為之前的圖片

    # 僅包含有時段的日子
    business_hours = ", ".join(f"{day}: {'、'.join(times)}" for day, times in hours.items() if times)

    update_restaurant_info(restaurant_info, restaurant_name, phone, address, business_hours, manager, manager_email, image_path)
    return {'success': '餐廳信息更新成功'}

def get_store_info_service(restaurant_id):
    store_info = get_store_info(restaurant_id)

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

def update_menu_item(item_id, item_name, price, description, status, item_image):
    item_info = get_item_info(item_id)

    if item_image and item_image.filename:
        # 處理圖片
        filename, file_extension = os.path.splitext(item_image.filename)
        filename = str(item_info.item_id) + file_extension
        image_path = os.path.join('images/menus', filename)  # 儲存相對路徑
        image_path = image_path.replace("\\", "/")  # 防止 Windows 路徑問題
        os.makedirs(os.path.dirname(os.path.join('./static', image_path)), exist_ok=True)  # 確保目錄存在
        item_image.save(os.path.join('./static', image_path))  # 儲存圖片
    else:
        image_path = item_info.item_image  # 若無圖片則設為上一張圖片

    update_item_info(item_info, item_name, price, description, status, image_path)
    return {'success': '餐點信息更新成功'}

def delete_menu_item(item_id):
    delete_item(item_id)
    return {'success': '餐點刪除成功'}