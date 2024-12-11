from app import db

# 用戶資料表
class UserTable(db.Model):
    __tablename__ = 'user_table'

    username = db.Column(db.String(50), primary_key=True, nullable=False, comment='用戶帳號，PK')
    password = db.Column(db.String(255), nullable=False, comment='用戶密碼')
    role = db.Column(db.Integer, nullable=False, comment='用戶角色（1顧客、2店家）')

# 顧客資料表
class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='顧客ID，自動遞增，PK')
    name = db.Column(db.String(100), nullable=False, comment='顧客姓名')
    phone = db.Column(db.String(20),  comment='顧客電話號碼')
    email = db.Column(db.String(100), nullable=False, comment='顧客電子郵件')
    
    username = db.Column(db.String(50), db.ForeignKey('user_table.username'), nullable=False, comment='對應用戶帳號（FK）')

# 店家資料表
class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    restaurant_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='店家ID，自動遞增，PK')
    restaurant_name = db.Column(db.String(100), nullable=False, comment='店家名稱')
    phone = db.Column(db.String(15), nullable=False, comment='店家電話號碼')
    address = db.Column(db.String(255), nullable=False, comment='店家地址')
    business_hours = db.Column(db.Text, nullable=False, comment='店家營業時間')
    manager = db.Column(db.String(50), nullable=False, comment='店家負責人')
    manager_email = db.Column(db.String(100), nullable=False, comment='店家負責人電子郵件')
    icon = db.Column(db.String(255), comment='店家圖示(URL)')
    
    username = db.Column(db.String(50), db.ForeignKey('user_table.username'), nullable=False, comment='對應用戶帳號（FK）')

# 餐點資料表
class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='餐點ID，自動遞增，PK')
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'), nullable=False, comment='所屬店家ID（FK）')
    item_name = db.Column(db.String(100), nullable=False, comment='餐點名稱')
    price = db.Column(db.Integer, nullable=False, comment='餐點價格')
    description = db.Column(db.String(255), comment='餐點描述')
    status = db.Column(db.Integer, nullable=False, default=1, comment='餐點狀態（0停售、1販售中）')
    item_image = db.Column(db.String(255), comment='餐點圖片(URL)')

# 訂單資料表
class OrderTable(db.Model):
    __tablename__ = 'order_table'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='訂單ID，自動遞增，PK')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False, comment='對應的顧客ID（FK）')
    order_status = db.Column(db.Integer, nullable=False, default=0, comment='訂單狀態（如：0下單前(在購物車中)、1待處理、2店家確認、3處理中、4已完成、5已刪除）')
    order_time = db.Column(db.DateTime, nullable=False, comment='訂單建立時間')
    total_amount = db.Column(db.Integer, nullable=False, comment='訂單總金額')
    order_pick_up_time = db.Column(db.DateTime, comment='訂單取餐時間')
    payment_method = db.Column(db.Integer, comment='付款方式（如：1現金、2信用卡）')
    payment_status = db.Column(db.Integer, nullable=False, default=0, comment='付款狀態（如：0未付款、1已付款）')
    order_note = db.Column(db.String(255), comment='訂單備註')

# 訂單明細表
class OrderDetail(db.Model):
    __tablename__ = 'order_detail'
    
    # 複合主鍵
    order_id = db.Column(db.Integer, db.ForeignKey('order_table.order_id'), primary_key=True, nullable=False, comment='對應的訂單ID')
    order_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='訂單明細ID')
    
    # 其他屬性
    item_id = db.Column(db.Integer, db.ForeignKey('menu_item.item_id'), nullable=False, comment='對應的餐點ID')
    item_price = db.Column(db.Integer, nullable=False, comment='餐點單價')
    quantity = db.Column(db.Integer, nullable=False, comment='購買的餐點數量')
    item_note = db.Column(db.String(255), comment='餐點備註')