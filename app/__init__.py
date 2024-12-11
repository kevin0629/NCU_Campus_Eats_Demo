from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import pymysql
import os

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.secret_key = os.urandom(24)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        # 導入模型 (延遲匯入)
        from .Repositories import Campus_Eats_Repository

        # 自動創建資料庫
        create_database(app)
        
        # 建立資料表
        db.create_all()

        
        # 延遲匯入controllers
        from .Controllers import Auth_Controller, Restaurant_Controller, Menu_Controller, Cart_Controller, Order_Controller
        # Register blueprints
        app.register_blueprint(Auth_Controller.auth_bp)
        app.register_blueprint(Cart_Controller.cart_bp)
        app.register_blueprint(Order_Controller.order_bp)
        app.register_blueprint(Restaurant_Controller.restaurant_bp)
        app.register_blueprint(Menu_Controller.menu_bp)


    return app

def create_database(app):
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    db_name = db_uri.split('/')[-1]
    connection_uri = '/'.join(db_uri.split('/')[:-1])
    connection = pymysql.connect(host='localhost', user='root', password='')
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET = 'utf8mb4'")
    connection.close()