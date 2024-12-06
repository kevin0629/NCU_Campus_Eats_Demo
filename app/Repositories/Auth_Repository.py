import hashlib
from sqlalchemy import desc
from app.Repositories.Campus_Eats_Repository import *
from app.Repositories import get_session

# 加密密碼
def encrypt_password(password):
    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    return encrypted_password

# 查詢用戶驗證，驗證登入用戶的帳號、密碼、角色是否正確可以登入
def is_authorized(username, password):
    encrypted_password = encrypt_password(password)
    with get_session() as db_session:
        user = db_session.query(UserTable).filter_by(username=username, password=encrypted_password).first()
        if user:
            return {
                'username': user.username,
                'role': user.role
            }
    return None

# 查詢該學號是否有在用戶資料表中
def is_user_exist(username):
    with get_session() as db_session:
        user_exists = db_session.query(UserTable).filter_by(username=username).first() is not None
    return user_exists

# 新增用戶
def add_user(username, password, role):
    encrypted_password = encrypt_password(password)
    with get_session() as db_session:
        new_user = UserTable(username=username, password=encrypted_password, role=role)
        db_session.add(new_user)
        db_session.commit()

# 新增顧客
def add_customer(name, phone, email, username):
    with get_session() as db_session:
        new_customer = Customer(name=name, phone=phone, email=email, username=username)
        db_session.add(new_customer)
        db_session.commit()

# 查詢顧客
def get_customer(username):
    with get_session() as db_session:
        customer = db_session.query(Customer).filter_by(username=username).first()
        if customer:
            return {
                'customer_id': customer.customer_id,
                'name': customer.name
            }
    return None

# 查詢店家
def get_restaurant(username):
    with get_session() as db_session:
        restaurant = db_session.query(Restaurant).filter_by(username=username).first()
        if restaurant:
            return {
                'restaurant_id': restaurant.restaurant_id,
                'restaurant_name': restaurant.restaurant_name,
                'icon': restaurant.icon
            }
    return None

# 新增店家
def add_restaurant(username, password, restaurant_name, phone, address, business_hours, manager, manager_email, image_path):
    encrypted_password = encrypt_password(password)
    with get_session() as db_session:
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

# 查詢最後一個店家
def get_last_store():
    with get_session() as db_session:
        return db_session.query(Restaurant).order_by(desc(Restaurant.restaurant_id)).first()

# 更新用戶密碼
def update_user_password(username, new_password):
    encrypted_password = encrypt_password(new_password)
    with get_session() as db_session:
        user = db_session.query(UserTable).filter_by(username=username).first()
        if user:
            user.password = encrypted_password
            db_session.commit()

# 查詢用戶
def get_user(username):
    with get_session() as db_session:
        return db_session.query(UserTable).filter_by(username=username).first()

# 查詢顧客
def get_customer_by_email(username, email):
    with get_session() as db_session:
        return db_session.query(Customer).filter_by(username=username, email=email).first()

# 查詢店家
def get_restaurant_by_email(username, email):
    with get_session() as db_session:
        return db_session.query(Restaurant).filter_by(username=username, manager_email=email).first()