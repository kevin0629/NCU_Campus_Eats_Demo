from app.Repositories.Campus_Eats_Repository import *
from app.Repositories import get_session

def get_all_restaurants():
    with get_session() as db_session:
        restaurants = db_session.query(Restaurant).all()
        return [
            {
                'restaurant_id': restaurant.restaurant_id,
                'restaurant_name': restaurant.restaurant_name,
                'phone': restaurant.phone,
                'address': restaurant.address,
                'business_hours': restaurant.business_hours,
                'icon': restaurant.icon
            }
            for restaurant in restaurants
        ]

def get_menu_items_by_restaurant_id(restaurant_id):
    with get_session() as db_session:
        menu_items = db_session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        return [
            {
                'item_id': item.item_id,
                'item_name': item.item_name,
                'price': item.price,
                'description': item.description,
                'status': item.status,
                'item_image': item.item_image
            }
            for item in menu_items
        ]

def get_restaurant_by_id(restaurant_id):
    with get_session() as db_session:
        restaurant = db_session.query(Restaurant).filter_by(restaurant_id=restaurant_id).first()
        if restaurant:
            return {
                'restaurant_id': restaurant.restaurant_id,
                'restaurant_name': restaurant.restaurant_name,
                'phone': restaurant.phone,
                'address': restaurant.address,
                'business_hours': restaurant.business_hours,
                'icon': restaurant.icon
            }
    return None

def get_menu_item_by_id(item_id):
    with get_session() as db_session:
        menu_item = db_session.query(MenuItem).filter_by(item_id=item_id).first()
        if menu_item:
            return {
                'item_id': menu_item.item_id,
                'item_name': menu_item.item_name,
                'price': menu_item.price,
                'description': menu_item.description,
                'status': menu_item.status,
                'item_image': menu_item.item_image
            }
    return None