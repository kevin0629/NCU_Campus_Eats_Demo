INSERT INTO `user_table` (`username`, `password`, `role`) VALUES
('113423027', 'c898b3c4675ed107b0f808d8903d747a73d813e0f2f6f25033c0090b8df6598d', 1),
('burger king', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 2),
('chicken master', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 2),
('eat breakfast', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 2),
('ImperialCity', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 2),
('kevinkuo', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 1),
('test', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 2),
('Yuloong', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 2);


INSERT INTO `customer` (`customer_id`, `name`, `phone`, `email`, `username`) VALUES
(1, '郭鎧菘', '0966514845', 'k113423027@g.ncu.edu.tw', 'kevinkuo'),
(2, '郭鎧菘', '0966514845', 'k113423027@g.ncu.edu.tw', '113423027');

INSERT INTO `restaurant` (`restaurant_id`, `restaurant_name`, `phone`, `address`, `business_hours`, `manager`, `manager_email`, `icon`, `username`) VALUES
(1, '炸雞大師', '03-427-5571', '桃園市中壢區中大路300號', 'Monday: 11:00~17:30, Tuesday: 11:00~17:30, Wednesday: 11:00~17:30, Thursday: 11:00~17:30, Friday: 11:00~17:30', 'Kevin', 'k113423027@g.ncu.edu.tw', 'images/restaurants/1.png', 'chicken master'),
(2, 'test', '0966514845', '桃園市中壢區中大路300號', 'Friday: 17:00~23:59', 'Kevin', 'k113423027@g.ncu.edu.tw', 'images/restaurants/restaurant.png', 'test'),
(3, '四海遊龍', '03-427-5429', '桃園市中壢區中大路300號', 'Monday: 11:00~20:00, Tuesday: 11:00~20:00, Wednesday: 11:00~20:00, Thursday: 11:00~20:00, Friday: 11:00~20:00', 'David', '410935010@gms.ndhu.edu.tw', 'images/restaurants/3.jpg', 'Yuloong'),
(4, '皇城滇緬料理', '0926-120-473', '桃園市中壢區中大路300號', 'Monday: 11:00~14:00, Tuesday: 11:00~14:00, Wednesday: 11:00~14:00, Thursday: 11:00~14:00, Friday: 11:00~14:00', 'Kevin', 'k113423027@g.ncu.edu.tw', 'images/restaurants/restaurant.png', 'ImperialCity'),
(5, '吃找餐', '0987-734-797', '桃園市中壢區中大路300號', 'Monday: 06:30~13:30, Tuesday: 06:30~13:30, Wednesday: 06:30~13:30, Thursday: 06:30~13:30, Friday: 06:30~13:30, Saturday: 08:00~13:00', 'David', '410935010@gms.ndhu.edu.tw', 'images/restaurants/restaurant.png', 'eat breakfast'),
(6, '漢堡王', '03-420-0832', '320桃園市中壢區中大路300號中央大學松苑餐廳1樓', 'Monday: 09:00~20:30, Tuesday: 09:00~20:30, Wednesday: 09:00~20:30, Thursday: 09:00~20:30, Friday: 09:00~20:30, Saturday: 09:00~20:30, Sunday: 09:00~20:30', 'David', '410935010@gms.ndhu.edu.tw', 'images/restaurants/6.jpg', 'burger king');

INSERT INTO `menu_item` (`item_id`, `item_name`, `price`, `description`, `status`, `item_image`, `restaurant_id`) VALUES
(3, '雞排', 85, 'It\'s good to eat.', 1, 'images/menus/1.jpg', 1),
(6, 'rice', 10, '', 0, 'images/menus/menu.png', 1),
(7, '嫩雞薯條', 69, '', 1, 'images/menus/7.jpg', 1),
(8, '台式甄寶蓋飯', 99, '', 1, 'images/menus/8.jpg', 1),
(9, '金桔檸檬', 40, 'It\'s good to drink.', 1, 'images/menus/9.jpg', 1),
(10, '獅紫薯薯', 39, '', 1, 'images/menus/10.jpg', 1),
(11, '台式椒鹽三寶蓋飯', 115, 'It\'s good to eat.', 1, 'images/menus/11.jpg', 1),
(12, '招牌鍋貼', 70, '10顆/1份', 1, 'images/menus/12.jpg', 3),
(13, '高麗菜水餃', 75, '10顆/1份', 1, 'images/menus/13.jpg', 3),
(14, '鮮蝦水餃', 110, '10顆/1份', 1, 'images/menus/14.jpg', 3),
(15, '韭菜鍋貼', 75, '10顆/1份', 1, 'images/menus/15.jpg', 3),
(16, 'egg', 10, '', 0, 'images/menus/menu.png', 3),
(17, '玉米濃湯', 35, '', 1, 'images/menus/menu.png', 3),
(18, '豆漿', 20, '', 1, 'images/menus/menu.png', 3),
(19, '豆漿', 20, '', 1, 'images/menus/menu.png', 5),
(20, '紅茶', 20, '', 1, 'images/menus/menu.png', 5),
(21, '招牌三明治', 50, '', 0, 'images/menus/menu.png', 5),
(22, '茶葉蛋', 15, 'It\'s good to eat.', 1, 'images/menus/menu.png', 5),
(23, '蔥抓餅', 40, '', 1, 'images/menus/menu.png', 5),
(24, '蔥抓餅加蛋', 50, 'It\'s good to eat.', 1, 'images/menus/menu.png', 5),
(25, '安格斯厚切牛肉堡', 145, 'It\'s good to eat.', 1, 'images/menus/25.png', 6),
(26, '重磅培根雙層牛肉堡', 219, '', 1, 'images/menus/26.png', 6),
(27, '薯條(中)', 59, '', 1, 'images/menus/menu.png', 6),
(28, '蘋果派', 49, '', 0, 'images/menus/menu.png', 6),
(29, '可樂(中)', 38, '', 1, 'images/menus/menu.png', 6),
(30, '雞塊', 75, '6塊', 1, 'images/menus/menu.png', 6),
(31, '辣味華堡', 134, '', 1, 'images/menus/31.png', 6),
(32, '椒麻雞飯', 150, '', 1, 'images/menus/32.jpg', 4),
(33, '打拋豬飯', 120, '', 1, 'images/menus/33.jpg', 4),
(34, '麻辣米線', 100, '', 1, 'images/menus/34.jpg', 4),
(35, '紅茶', 20, '', 0, 'images/menus/menu.png', 4),
(36, '綠咖哩雞飯', 120, '', 1, 'images/menus/36.jpg', 4),
(37, '咖哩雞飯', 120, '', 1, 'images/menus/37.jpg', 4),
(38, 'egg', 10, '', 0, 'images/menus/menu.png', 4);