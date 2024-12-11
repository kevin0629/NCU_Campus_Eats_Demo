from app.Repositories.Menu_Repository import *
from datetime import datetime

# 獲取營業中的店家
def get_open_stores_service(db_session, current_day, current_time):
    store_info = get_all_restaurants_service(db_session)

    valid_stores = []

    for store in store_info:
        raw_business_hours = store['business_hours']
        if not raw_business_hours:
            continue  # 無營業時間資料的店家跳過

        try:
            # 找出當天的營業時間
            today_hours = next(
                (times for day, times in (entry.split(": ") for entry in raw_business_hours.split(", ")) if day == current_day),
                None
            )
            if not today_hours:
                continue  # 如果當天無營業時間則跳過
        except ValueError:
            continue  # 格式錯誤的營業時間跳過

        # 分割時間區間並檢查是否符合當前時間
        is_open = False
        for time_range in today_hours.split("、"):
            try:
                start, end = map(lambda t: datetime.strptime(t.strip(), "%H:%M").time(), time_range.split("~"))
                if start <= end:
                    if start <= current_time <= end:
                        is_open = True
                        break
                else:  # 處理跨午夜的情況
                    if current_time >= start or current_time <= end:
                        is_open = True
                        break
            except ValueError:
                continue  # 格式錯誤的時間區間跳過

        if is_open:
            valid_stores.append({
                "restaurant_id": store['restaurant_id'],
                "restaurant_name": store['restaurant_name'],
                "phone": store['phone'],
                "address": store['address'],
                "business_hours": store['business_hours'],
                "icon": store['icon']
            })

    return valid_stores

def get_all_restaurants_service(db_session):
    return get_all_restaurants(db_session)

def get_menu_items_by_restaurant_id_service(db_session, restaurant_id):
    return get_menu_items_by_restaurant_id(db_session, restaurant_id)

def get_restaurant_by_id_service(db_session, restaurant_id):
    return get_restaurant_by_id(db_session, restaurant_id)

