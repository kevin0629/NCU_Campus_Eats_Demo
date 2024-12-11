import hashlib
from sqlalchemy import desc
from app.Repositories.Campus_Eats_Repository import *

# 1.1 新增用戶
def add_user(db_session, username, password, role):
    encrypted_password = encrypt_password(password)
    new_user = UserTable(username=username, password=encrypted_password, role=role)
    db_session.add(new_user)
    db_session.commit()

# 1.1 新增顧客
def add_customer(db_session, name, phone, email, username):
    new_customer = Customer(name=name, phone=phone, email=email, username=username)
    db_session.add(new_customer)
    db_session.commit()

# 1.1 新增店家
def add_restaurant(db_session, username, password, restaurant_name, phone, address, business_hours, manager, manager_email, image_path):
    encrypted_password = encrypt_password(password)
    new_user = UserTable(username=username, password=encrypted_password, role=2)
    db_session.add(new_user)
    db_session.commit()  # 確保新用戶已經插入

    new_restaurant = Restaurant(
        restaurant_name=restaurant_name,
        phone=phone,
        address=address,
        business_hours=business_hours,
        manager=manager,
        manager_email=manager_email,
        icon=image_path,
        username=username
    )
    db_session.add(new_restaurant)
    db_session.commit()

# 1.1 查詢最後一個店家
def get_last_store(db_session):
    return db_session.query(Restaurant).order_by(desc(Restaurant.restaurant_id)).first()

# 1.1 + 1.2 查詢顧客
def get_customer(db_session, username):
    customer = db_session.query(Customer).filter_by(username=username).first()
    if customer:
        return {
            'customer_id': customer.customer_id,
            'name': customer.name
        }
    return None

# 1.2 查詢用戶驗證，驗證登入用戶的帳號、密碼、角色是否正確可以登入
def is_authorized(db_session, username, password):
    encrypted_password = encrypt_password(password)
    user = db_session.query(UserTable).filter_by(username=username, password=encrypted_password).first()
    if user:
        return {
            'username': user.username,
            'role': user.role
        }
    return None

# 1.2 查詢店家
def get_restaurant(db_session, username):
    restaurant = db_session.query(Restaurant).filter_by(username=username).first()
    if restaurant:
        return {
            'restaurant_id': restaurant.restaurant_id,
            'restaurant_name': restaurant.restaurant_name,
            'icon': restaurant.icon
        }
    return None

# 1.4 更新用戶密碼
def update_user_password(db_session, username, new_password):
    encrypted_password = encrypt_password(new_password)
    user = db_session.query(UserTable).filter_by(username=username).first()
    if user:
        user.password = encrypted_password
        db_session.commit()

# 1.4 查詢用戶
def get_user(db_session, username):
    return db_session.query(UserTable).filter_by(username=username).first()

# 1.4 查詢顧客
def get_customer_by_email(db_session, username, email):
    return db_session.query(Customer).filter_by(username=username, email=email).first()

# 1.4 查詢店家
def get_restaurant_by_email(db_session, username, email):
    return db_session.query(Restaurant).filter_by(username=username, manager_email=email).first()

# 1.5 + 1.6 抓取原始的顧客資料
def get_customer_info(db_session, customer_id):
    return db_session.query(Customer).filter_by(customer_id=customer_id).first()

# 1.6 更新顧客資料
def update_customer_info(db_session, customer, new_name, new_phone, new_email):
    if customer.name != new_name:
        customer.name = new_name
    if customer.phone != new_phone:
        customer.phone = new_phone
    if customer.email != new_email:
        customer.email = new_email
    db_session.commit()

# 加密密碼
def encrypt_password(password):
    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    return encrypted_password

