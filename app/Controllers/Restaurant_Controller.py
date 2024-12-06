import os
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from app.Services.Restaurant_Service import *

restaurant_bp = Blueprint('restaurants', __name__, template_folder='templates/restaurants', static_folder='./static')

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

        result = add_menu_item(restaurant_id, item_name, price, description, status, item_image)
        if 'error' in result:
            flash(result['error'])
            return redirect(url_for('restaurants.add_item'))
        else:
            return redirect(url_for('menus.view_menu', restaurant_id=restaurant_id))
    
    essential_data = {"restaurant_id": session.get('restaurant_id'), "restaurant_name": session.get('restaurant_name'), "icon": session.get('icon')}

    return render_template('restaurants/add_item.html', **essential_data)

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

        result = update_store_info(restaurant_id, restaurant_name, phone, address, manager, manager_email, icon, hours)
        if 'success' in result:
            session['restaurant_name'] = restaurant_name
            session['icon'] = icon.filename if icon and icon.filename else session['icon']
            flash(result['success'])
        return redirect(url_for('menus.view_menu', restaurant_id=restaurant_id))

    return render_template('restaurants/profile.html')

@restaurant_bp.route('/management/view_store_info')
def view_store_info():
    restaurant_id = session.get('restaurant_id')
    store_data = get_store_info_service(restaurant_id)
    return render_template('restaurants/profile.html', **store_data)

@restaurant_bp.route('/management/modify_item/<int:item_id>', methods=['GET', 'POST'])
def modify_item(item_id):
    if request.method == "POST":
        item_name = request.form['item_name']
        price = request.form['price']
        description = request.form['description']
        status = request.form['status']
        item_image = request.files['item_image']

        result = update_menu_item(item_id, item_name, price, description, status, item_image)
        if 'success' in result:
            flash(result['success'])
        return redirect(url_for('menus.view_menu', restaurant_id=session.get('restaurant_id')))

@restaurant_bp.route('/management/delete_item/<int:item_id>')
def delete_item(item_id):
    result = delete_menu_item(item_id)
    if 'success' in result:
        flash(result['success'])
    return redirect(url_for('menus.view_menu', restaurant_id=session.get('restaurant_id')))