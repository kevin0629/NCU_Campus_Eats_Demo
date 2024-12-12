import os, re, random, string
from flask import current_app
from flask_mail import Message
from app.Repositories.Auth_Repository import *
from app import mail

# 1.1 註冊用戶
def register_user_service(db_session, data, icon):
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    email = data.get('email') if role == 'customer' else data.get('manager_email')

    if password != confirm_password:
        return {'error': '密碼和確認密碼不一致'}

    if not is_valid_email(email):
        return {'error': '無效的電子郵件格式'}
    
    user_exists = get_user(db_session, username)
    if user_exists:
        return {'error': '帳號已存在'}

    if role == 'customer':
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')

        add_user(db_session, username, password, 1)
        add_customer(db_session, name, phone, email, username)

        return {'success': '顧客註冊成功！'}

    elif role == 'restaurant':
        restaurant_name = data.get('restaurant_name')
        phone = data.get('phone')
        address = data.get('address')
        manager = data.get('manager')
        manager_email = data.get('manager_email')

        if icon and icon.filename:
            last_store = get_last_store(db_session)
            store_id = 0 if last_store is None else last_store.restaurant_id

            # 處理圖片
            filename, file_extension = os.path.splitext(icon.filename)
            filename = str(store_id + 1) + file_extension
            image_path = os.path.join('images/restaurants', filename)  # 儲存相對路徑
            image_path = image_path.replace("\\", "/")
            os.makedirs(os.path.dirname(os.path.join('./app/static', image_path)), exist_ok=True)  # 確保目錄存在
            icon.save(os.path.join('./app/static', image_path))  # 儲存圖
        else:
            image_path = 'images/restaurants/restaurant.png'   # 若無圖片則設為設定預設圖片

        hours = {}
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            times = data.getlist(f"{day}[]")
            hours[day] = [time for time in times if time]  # 過濾空值

        # 僅包含有時段的日子
        business_hours = ", ".join(f"{day}: {'、'.join(times)}" for day, times in hours.items() if times)

        add_restaurant(db_session, username, password, restaurant_name, phone, address, business_hours, manager, manager_email, image_path)

        return {'success': '店家註冊成功！'}

# 1.2 驗證用戶
def authenticate_user_service(db_session, username, password):
    user = is_authorized(db_session, username, password)
    if user:
        if user['role'] == 1:
            customer = get_customer(db_session, username)
            return {
                'username': user['username'],
                'role': user['role'],
                'customer_id': customer['customer_id'],
                'customer_name': customer['name']
            }
        elif user['role'] == 2:
            restaurant = get_restaurant(db_session, username)
            return {
                'username': user['username'],
                'role': user['role'],
                'restaurant_id': restaurant['restaurant_id'],
                'restaurant_name': restaurant['restaurant_name'],
                'icon': restaurant['icon']
            }
    return None

# 1.4 重設密碼(暫時密碼)
def reset_password_service(db_session, username, email):
    user = get_user(db_session, username)
    if user:
        if user.role == 1:  # 顧客
            customer = get_customer_by_email(db_session, username, email)
            if not customer:
                return {'error': '帳號或電子郵件不正確。'}
        elif user.role == 2:  # 店家
            restaurant = get_restaurant_by_email(db_session, username, email)
            if not restaurant:
                return {'error': '帳號或電子郵件不正確。'}
        
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        msg = Message('重置密碼', sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        msg.body = f'您的新密碼是：{new_password}'

        try:
            mail.send(msg)
            update_user_password(db_session, username, new_password)
            return {'success': '新密碼已發送到您的電子郵件。'}
        except Exception as e:
            return {'error': '無法發送電子郵件，請稍後再試。'}
    else:
        return {'error': '帳號或電子郵件不正確。'}

# 1.4 修改密碼
def change_password_service(db_session, username, current_password, new_password, confirm_password):
    if new_password != confirm_password:
        return {'error': '新密碼和確認密碼不一致'}

    user = get_user(db_session, username)
    if user and user.password == encrypt_password(current_password):
        update_user_password(db_session, username, new_password)
        return {'success': '密碼修改成功'}
    else:
        return {'error': '當前密碼不正確'}
    
# 1.5 取得顧客資料Service
def get_customer_profile_service(db_session, customer_id):
    return get_customer_info(db_session, customer_id)

# 1.6 更新顧客資料Service
def update_customer_profile_service(db_session, customer_id, new_name, new_phone, new_email):
    customer = get_customer_info(db_session, customer_id)
    if customer:
        update_customer_info(db_session, customer, new_name, new_phone, new_email)
        return True
    return False

# 驗證email格式
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


