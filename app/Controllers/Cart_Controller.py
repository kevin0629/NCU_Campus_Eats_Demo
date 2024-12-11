from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.Services.Cart_Service import *

cart_bp = Blueprint('carts', __name__, static_folder='./static')

# 4.1 新增餐點進購物車
@cart_bp.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    if request.method == 'POST':
        item_id = request.form['item_id']
        item_price = request.form['item_price']
        redirect_flag = int(request.form.get('redirect_flag'))
        customer_id = session.get('customer_id')

        with get_session() as db_session:
            restaurant_id = add_item_to_cart(db_session, item_id, item_price, customer_id)
            if redirect_flag == 1:
                return redirect(url_for('carts.view_cart'))
            else:
                return redirect(url_for('menus.view_menu', restaurant_id=restaurant_id))
        
# 4.2 查看購物車內容
@cart_bp.route('/view_cart')
def view_cart():
    customer_id = session.get('customer_id')
    customer_name = session.get('customer_name')
    with get_session() as db_session:
        order_list = get_cart_items(db_session, customer_id)
    return render_template('customers/view_cart.html', cart_items=order_list, customer_name=customer_name)

# 4.3 移除一個商品
@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        order_id = request.form['order_id']
        order_detail_id = request.form['order_detail_id']
        with get_session() as db_session:
            remove_item_from_cart(db_session, order_id, order_detail_id)
    return redirect(url_for('carts.view_cart'))

