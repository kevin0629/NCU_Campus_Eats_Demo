import os
import random
import string
from flask import current_app
from flask_mail import Message
from app.Repositories.Auth_Repository import *
from app import mail

def authenticate_user(username, password):
    user = is_authorized(username, password)
    if user:
        if user['role'] == 1:
            customer = get_customer(username)
            return {
                'username': user['username'],
                'role': user['role'],
                'customer_id': customer['customer_id'],
                'customer_name': customer['name']
            }
        elif user['role'] == 2:
            restaurant = get_restaurant(username)
            return {
                'username': user['username'],
                'role': user['role'],
                'restaurant_id': restaurant['restaurant_id'],
                'restaurant_name': restaurant['restaurant_name'],
                'icon': restaurant['icon']
            }
    return None

def register_user(data):
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        return {'error': '密碼和確認密碼不一致'}

    user_exists = is_user_exist(username)
    if user_exists:
        return {'error': '帳號已存在'}

    if role == 'customer':
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')

        add_user(username, password, 1)
        add_customer(name, phone, email, username)

        return {'success': '顧客註冊成功！'}

    elif role == 'restaurant':
        restaurant_name = data.get('restaurant_name')
        phone = data.get('phone')
        address = data.get('address')
        manager = data.get('manager')
        manager_email = data.get('manager_email')
        icon = data.get('icon')

        if icon and icon.filename:
            last_store = get_last_store()
            store_id = 0 if last_store is None else last_store.restaurant_id

            # 處理圖片
            filename, file_extension = os.path.splitext(icon.filename)
            filename = str(store_id + 1) + file_extension
            image_path = os.path.join('static/images/restaurants', filename)  # 儲存相對路徑
            image_path = image_path.replace("\\", "/")
            os.makedirs(os.path.dirname(image_path), exist_ok=True)  # 確保目錄存在
            icon.save(image_path)  # 儲存圖片
        else:
            image_path = 'static/images/restaurants/restaurant.png'  # 若無圖片則設為設定預設圖片

        hours = {}
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            times = data.getlist(f"{day}[]")
            hours[day] = [time for time in times if time]  # 過濾空值

        # 僅包含有時段的日子
        business_hours = ", ".join(f"{day}: {'、'.join(times)}" for day, times in hours.items() if times)

        add_restaurant(username, password, restaurant_name, phone, address, business_hours, manager, manager_email, image_path)

        return {'success': '店家註冊成功！'}

def reset_password(username, email):
    user = get_user(username)
    if user:
        if user.role == 1:  # 顧客
            customer = get_customer_by_email(username, email)
            if not customer:
                return {'error': '帳號或電子郵件不正確。'}
        elif user.role == 2:  # 店家
            restaurant = get_restaurant_by_email(username, email)
            if not restaurant:
                return {'error': '帳號或電子郵件不正確。'}

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        encrypted_password = encrypt_password(new_password)

        msg = Message('重置密碼', sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        msg.body = f'您的新密碼是：{new_password}'

        try:
            mail.send(msg)
            update_user_password(username, new_password)
            return {'success': '新密碼已發送到您的電子郵件。'}
        except Exception as e:
            return {'error': '無法發送電子郵件，請稍後再試。'}
    else:
        return {'error': '帳號或電子郵件不正確。'}

def change_password(username, current_password, new_password, confirm_password):
    if new_password != confirm_password:
        return {'error': '新密碼和確認密碼不一致'}

    user = get_user(username)
    if user and user.password == encrypt_password(current_password):
        update_user_password(username, new_password)
        return {'success': '密碼修改成功'}
    else:
        return {'error': '當前密碼不正確'}