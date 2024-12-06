from app.Repositories.Campus_Eats_Repository import *
from app.Repositories import get_session
from sqlalchemy import desc

def item_exists(restaurant_id, item_name):
    with get_session() as db_session:
        return db_session.query(MenuItem).filter_by(item_name=item_name, restaurant_id=restaurant_id).first() is not None

def get_last_item():
    with get_session() as db_session:
        return db_session.query(MenuItem).order_by(desc(MenuItem.item_id)).first()

def add_item(restaurant_id, item_name, price, description, status, image_path):
    with get_session() as db_session:
        new_item = MenuItem(item_name=item_name, price=price, description=description, status=status, item_image=image_path, restaurant_id=restaurant_id)
        db_session.add(new_item)
        db_session.commit()

def get_restaurant_info(restaurant_id):
    with get_session() as db_session:
        return db_session.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()

def update_restaurant_info(restaurant_info, restaurant_name, phone, address, business_hours, manager, manager_email, image_path):
    with get_session() as db_session:
        restaurant_info.restaurant_name = restaurant_name
        restaurant_info.phone = phone
        restaurant_info.address = address
        restaurant_info.business_hours = business_hours
        restaurant_info.manager = manager
        restaurant_info.manager_email = manager_email
        restaurant_info.icon = image_path
        db_session.commit()

def get_store_info(restaurant_id):
    with get_session() as db_session:
        return db_session.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()

def get_item_info(item_id):
    with get_session() as db_session:
        return db_session.query(MenuItem).filter_by(item_id=item_id).first()

def update_item_info(item_info, item_name, price, description, status, image_path):
    with get_session() as db_session:
        item_info.item_name = item_name
        item_info.price = price
        item_info.description = description
        item_info.status = status
        item_info.item_image = image_path
        db_session.commit()

def delete_item(item_id):
    with get_session() as db_session:
        item_info = db_session.query(MenuItem).filter_by(item_id=item_id).first()
        db_session.delete(item_info)
        db_session.commit()