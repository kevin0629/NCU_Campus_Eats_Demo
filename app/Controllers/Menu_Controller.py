from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, current_app
from app.Services.Menu_Service import *
from app.Repositories import get_session

menu_bp = Blueprint('menus', __name__, static_folder='./static')

# 菜單頁面
@menu_bp.route('/menu')
def menu():
    return render_template('customers/view_store.html')

# 3.1 顧客首頁看到正在營業中的店家
@menu_bp.route('/view_store')
def view_store():
    if not session.get('role'):
        return redirect(url_for('auth.login'))

    # 定義台灣時區
    taiwan_tz = timezone(timedelta(hours=+8))

    # 取得當前台灣的日期和時間
    now = datetime.now(taiwan_tz)
    current_day = now.strftime("%A")  # 當前星期
    current_time = now.time()  # 當前時間

    with get_session() as db_session:
        # 呼叫 service 獲取營業中的店家
        valid_stores = get_open_stores_service(db_session, current_day, current_time)

        # 將營業中的店家資料傳遞到模板
        data = {
            "customer_name": session.get('customer_name'),
            "openedRestaurants": valid_stores
        }

    return render_template('customers/view_store.html', **data)

# 3.2 查看店家菜單
@menu_bp.route('/view_menu/<int:restaurant_id>')
def view_menu(restaurant_id):
    role = session.get('role')
    if not role:
        return redirect(url_for('auth.login'))
    with get_session() as db_session:
        menu_info = get_menu_items_by_restaurant_id_service(db_session, restaurant_id)
        restaurant_info = get_restaurant_by_id_service(db_session, restaurant_id)
        
        restaurant_data = {
            "restaurant_name": restaurant_info['restaurant_name'],
            "phone": restaurant_info['phone'],
            "address": restaurant_info['address'],
            "business_hours": restaurant_info['business_hours'],
            "icon": restaurant_info['icon']
        }
        # 將 MenuItem 的資料提取為字典
        menu_items = [
            {
                "item_id": item['item_id'],
                "item_name": item['item_name'],
                "price": item['price'],
                "description": item['description'],
                "status": item['status'],
                "item_image": item['item_image']
            }
            for item in menu_info
        ]

    if role == 1:
        data = {
            "username": session.get('username'),
            "customer_id": session.get('customer_id'),
            "customer_name": session.get('customer_name'),
            "restaurant": restaurant_data,
            "menu_items": menu_items  # 使用轉換過的資料
        }
        return render_template('customers/view_menu.html', **data)
    else:
        # 包裝資料以傳遞給模板
        data = {
            "restaurant_id": restaurant_id,
            "restaurant_name": session.get('restaurant_name'),
            "icon": session.get('icon'),
            "menu_items": menu_items  # 使用轉換過的資料
        }
        return render_template('restaurants/management.html', **data)

