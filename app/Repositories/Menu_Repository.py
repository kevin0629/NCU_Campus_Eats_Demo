from app.Repositories.Campus_Eats_Repository import *
from app.Repositories import get_session

def get_all_restaurants(db_session):
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

def get_menu_items_by_restaurant_id(db_session, restaurant_id):
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

def get_restaurant_by_id(db_session, restaurant_id):
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
