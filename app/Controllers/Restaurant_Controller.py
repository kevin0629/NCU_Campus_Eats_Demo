import os
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from app.Services.Restaurant_Service import *

restaurant_bp = Blueprint('restaurants', __name__, template_folder='templates/restaurants', static_folder='./static')

# 餐廳相關==============================================================================================================
# 2.1 查看餐廳資訊
@restaurant_bp.route('/management/view_store_info')
def view_store_info():
    restaurant_id = session.get('restaurant_id')
    with get_session() as db_session:
        store_data = get_store_info_service(db_session, restaurant_id)
    return render_template('restaurants/profile.html', **store_data)

# 2.2 修改餐廳資訊
@restaurant_bp.route('/management/edit_store_info', methods=['GET', 'POST'])
def edit_store_info():
    if request.method == "POST":
        restaurant_id = session.get('restaurant_id')

        restaurant_name = request.form['restaurant_name']
        phone = request.form['phone']
        address = request.form['address']
        manager = request.form['manager']
        manager_email = request.form['manager_email']
        icon = request.files['icon']

        hours = {}
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            times = request.form.getlist(f"{day}[]")
            hours[day] = [time for time in times if time]  # 過濾空值

        with get_session() as db_session:
            result = update_store_info(db_session, restaurant_id, restaurant_name, phone, address, manager, manager_email, icon, hours)
            if 'success' in result:
                session['restaurant_name'] = restaurant_name
                session['icon'] = result['icon']
                flash(result['success'])
        return redirect(url_for('menus.view_menu', restaurant_id=restaurant_id))

    return render_template('restaurants/profile.html')

# 餐點相關==============================================================================================================

# 2.3 新增餐點
@restaurant_bp.route('/management/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # 從 session 取得資料
        restaurant_id = session.get('restaurant_id')

        item_name = request.form['item_name']
        price = request.form['price']
        description = request.form['description']
        status = request.form['status']
        item_image = request.files['item_image']

        with get_session() as db_session:
            result = add_menu_item(db_session, restaurant_id, item_name, price, description, status, item_image)
            if 'error' in result:
                flash(result['error'])
                return redirect(url_for('restaurants.add_item'))
            else:
                return redirect(url_for('menus.view_menu', restaurant_id=restaurant_id))
    
    essential_data = {"restaurant_id": session.get('restaurant_id'), "restaurant_name": session.get('restaurant_name'), "icon": session.get('icon')}

    return render_template('restaurants/add_item.html', **essential_data)

# 2.4 店家查看各餐點資訊頁面
@restaurant_bp.route('/view_detailed_menu/<int:item_id>')
def view_detailed_menu(item_id):
    with get_session() as db_session:
        menu_info = get_menu_item_by_id_service(db_session, item_id)

        data = {
                "restaurant_id": session.get('restaurant_id'),
                "restaurant_name": session.get('restaurant_name'),
                "icon": session.get('icon'),
                "item_id": menu_info['item_id'],
                "item_name": menu_info['item_name'],
                "price": menu_info['price'],
                "description": menu_info['description'],
                "status": menu_info['status'],
                "item_image": menu_info['item_image']
            }

    return render_template('restaurants/modify_item.html', **data)

# 2.4 修改餐點
@restaurant_bp.route('/management/modify_item/<int:item_id>', methods=['GET', 'POST'])
def modify_item(item_id):
    if request.method == "POST":
        item_name = request.form['item_name']
        price = request.form['price']
        description = request.form['description']
        status = request.form['status']
        item_image = request.files['item_image']

        with get_session() as db_session:
            result = update_menu_item(db_session, item_id, item_name, price, description, status, item_image)
            if 'success' in result:
                flash(result['success'])
            return redirect(url_for('menus.view_menu', restaurant_id=session.get('restaurant_id')))

# 2.5 刪除餐點
@restaurant_bp.route('/management/delete_item/<int:item_id>')
def delete_item(item_id):
    with get_session() as db_session:
        result = delete_menu_item(db_session, item_id)
        if 'success' in result:
            flash(result['success'])
    return redirect(url_for('menus.view_menu', restaurant_id=session.get('restaurant_id')))

# 訂單相關==============================================================================================================

# 2.6 查看訂單
@restaurant_bp.route('/management/view_order')
def view_order():
    restaurant_id = session.get('restaurant_id')
    with get_session() as db_session:
        order_process = get_pending_orders_service(db_session, restaurant_id)
        essential_data = {"restaurant_id": restaurant_id, "restaurant_name": session.get('restaurant_name'), "icon": session.get('icon'), "order_process": order_process}
    return render_template('restaurants/view_order.html', **essential_data)

# 2.7 查看歷史訂單
@restaurant_bp.route('/management/view_history_order')
def view_history_order():
    restaurant_id = session.get('restaurant_id')
    with get_session() as db_session:
        history_order = get_history_orders_service(db_session, restaurant_id)
    essential_data = {"restaurant_id": restaurant_id, "restaurant_name": session.get('restaurant_name'), "icon": session.get('icon'), "history_order": history_order}
    return render_template('restaurants/view_history_order.html', **essential_data)

# 2.8 更新訂單狀態
@restaurant_bp.route('/management/view_order/update_order_status', methods=['POST'])
def update_order_status():
    order_status = request.form['order_status']
    order_id = request.form['order_id']
    with get_session() as db_session:
        update_order_status_service(db_session, order_id, order_status)
    return redirect(url_for('restaurants.view_order'))

# 2.9 更新付款狀態
@restaurant_bp.route('/management/view_order/update_payment_status', methods=['POST'])
def update_payment_status():
    order_id = request.form['payment_order_id']
    payment_status = request.form['payment_status']
    with get_session() as db_session:
        update_payment_status_service(db_session, order_id, payment_status)
    return redirect(url_for('restaurants.view_order'))

