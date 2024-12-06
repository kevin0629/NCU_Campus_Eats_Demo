from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.Services.Customer_Service import *

customer_bp = Blueprint('customers', __name__, template_folder='templates/customers', static_folder='./static')

# 菜單頁面
@customer_bp.route('/menu')
def menu():
    return render_template('customers/view_store.html')

# 新增餐點進購物車
@customer_bp.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    if request.method == 'POST':
        item_id = request.form['item_id']
        item_price = request.form['item_price']
        redirect_flag = int(request.form.get('redirect_flag'))
        customer_id = session.get('customer_id')

        redirect_flag, restaurant_id = add_item_to_cart(item_id, item_price, customer_id, redirect_flag)
        if redirect_flag == 1:
            return redirect(url_for('customers.view_cart'))
        else:
            return redirect(url_for('menus.view_menu', restaurant_id=restaurant_id))
        
# 查看購物車內容
@customer_bp.route('/view_cart')
def view_cart():
    customer_id = session.get('customer_id')
    customer_name = session.get('customer_name')
    order_list = get_cart_items(customer_id)
    return render_template('customers/view_cart.html', cart_items=order_list, customer_name=customer_name)

# 移除一個商品
@customer_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        order_id = request.form['order_id']
        order_detail_id = request.form['order_detail_id']
        remove_item_from_cart(order_id, order_detail_id)
    return redirect(url_for('customers.view_cart'))

# 刪除整筆購物車
@customer_bp.route('/delete_order', methods=['POST'])
def delete_order():
    order_id = request.form['order_id']
    if not order_id:
        flash('無效的訂單 ID', 'error')
        return redirect(url_for('customers.view_order'))
    else:
        IsDeleted = delete_order_from_cart(order_id)
        if IsDeleted:
            flash('訂單狀態已送回！', 'success')
        else:
            flash('未找到該訂單，請檢查後再試。', 'error')

    return redirect(url_for('customers.view_cart'))

# 送出訂單
@customer_bp.route('/checkout_order', methods=['POST'])
def checkout_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        total_price = request.form['total_price']
        pickup_time = request.form['pickup_time'] # 取餐時間
        payment_method = request.form['payment_method'] # 新增獲取付款方式

        checkout_order_service(order_id, total_price, pickup_time, payment_method)
    return redirect(url_for('customers.view_cart'))

# 查看歷史已送出之訂單
@customer_bp.route('/view_order')
def view_order():
    customer_name = session.get('customer_name')
    customer_id = session.get('customer_id')
    order_all_list = get_all_orders(customer_id)
    return render_template('customers/view_order.html', customer_name=customer_name, order_all_list=order_all_list)

# 修改訂單狀態回到退回狀態
@customer_bp.route('/return_order', methods=['POST'])
def return_order():
    order_id = request.form['order_id']
    restaurant_id = int(request.form['restaurant_id'])
    customer_id = session.get('customer_id')
    
    IsReturn = return_order_service(order_id, restaurant_id, customer_id)
    if not IsReturn:
        flash('已有相同店家未送出的訂單，無法將此訂單退回到修改狀態。', 'error')
        
    return redirect(url_for('customers.view_order'))

# 抓取原始的個人資料
@customer_bp.route('/view_pf')
def view_pf():
    customer_id = session.get('customer_id')
    customer_name = session.get('customer_name')
    data = get_customer_profile(customer_id)
    if not data:
        flash("找不到您的資料，請重新登錄", "error")
        return redirect(url_for('auth.login'))
    customer_data = {
        "name": data.name,
        "phone": data.phone,
        "email": data.email
    }
    return render_template('customers/view_customer_pf.html', customer_name=customer_name, customer_pf=customer_data)

# 獲取當前客戶信息
@customer_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    customer_id = session.get('customer_id')
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_phone = request.form.get('phone')
        new_email = request.form.get('email')
        if update_customer_profile(customer_id, new_name, new_phone, new_email):
            flash("您的個人資料已成功更新！", "success")
        else:
            flash("無法找到您的個人資料，請重新登錄。", "error")
    return redirect(url_for('customers.view_pf'))

# 新增備註
@customer_bp.route('/add_note', methods=['POST'])
def add_note():
    customer_id = session.get('customer_id')
    order_id = request.form.get('order_id')
    order_detail_id = request.form.get('order_detail_id')
    note_text = request.form.get('note')
    if not note_text:
        flash("請輸入備註內容", "error")
        return redirect(url_for('customers.view_cart'))
    success = add_note_service(order_id, order_detail_id, note_text)
    if success:
        flash("備註新增成功！", "success")
    else:
        flash("找不到訂單或訂單細項，請重試", "error")
    return redirect(url_for('customers.view_cart'))