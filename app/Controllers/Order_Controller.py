from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.Services.Order_Service import *
from app.Repositories import get_session

order_bp = Blueprint('orders', __name__, static_folder='./static')

# 5.1 + 5.2查看歷史已送出之訂單
@order_bp.route('/view_order')
def view_order():
    customer_name = session.get('customer_name')
    customer_id = session.get('customer_id')
    with get_session() as db_session:
        order_all_list = get_all_orders(db_session, customer_id)
        return render_template('customers/view_order.html', customer_name=customer_name, order_all_list=order_all_list)

# 5.3 + 5.6 送出訂單
@order_bp.route('/checkout_order', methods=['POST'])
def checkout_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        total_price = request.form['total_price']
        pickup_time = request.form['pickup_time'] # 取餐時間
        payment_method = request.form['payment_method'] # 新增獲取付款方式
        with get_session() as db_session:
            checkout_order_service(db_session, order_id, total_price, pickup_time, payment_method)
    return redirect(url_for('carts.view_cart'))


# 5.3.2新增訂單備註
@order_bp.route('/add_note', methods=['POST'])
def add_note():
    # customer_id = session.get('customer_id')
    order_id = request.form.get('order_id')
    order_detail_id = request.form.get('order_detail_id')
    note_text = request.form.get('note')
    if not note_text:
        flash("請輸入備註內容", "error")
        return redirect(url_for('carts.view_cart'))
    with get_session() as db_session:
        success = add_note_service(db_session, order_id, order_detail_id, note_text)
        if success:
            flash("備註新增成功！", "success")
        else:
            flash("找不到訂單或訂單細項，請重試", "error")
    return redirect(url_for('carts.view_cart'))


# 5.4 修改訂單狀態回到退回狀態
@order_bp.route('/return_order', methods=['POST'])
def return_order():
    order_id = request.form['order_id']
    restaurant_id = int(request.form['restaurant_id'])
    customer_id = session.get('customer_id') # 目前使用者 id
    
    with get_session() as db_session:
        IsReturn = return_order_service(db_session, order_id, restaurant_id, customer_id)
        if not IsReturn:
            flash('已有相同店家未送出的訂單，無法將此訂單退回到修改狀態。', 'error')
        
    return redirect(url_for('orders.view_order'))

# 5.5 刪除整筆購物車
@order_bp.route('/delete_order', methods=['POST'])
def delete_order():
    order_id = request.form['order_id']
    if not order_id:
        flash('無效的訂單 ID', 'error')
        return redirect(url_for('carts.view_order'))
    else:
        with get_session() as db_session:
            IsDeleted = delete_order_from_cart(db_session, order_id)
            if IsDeleted:
                flash('訂單狀態已送回！', 'success')
            else:
                flash('未找到該訂單，請檢查後再試。', 'error')

    return redirect(url_for('carts.view_cart'))