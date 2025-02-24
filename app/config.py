import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://****:*@localhost/campus_eats'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://****:*********@mysql-1.cfg8ygkqmlab.ap-northeast-3.rds.amazonaws.com/campus_eats' #AWS
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OAuth 設定
    CLIENT_ID = '20241007203637hgWIOoOg6QGH'  # 從中央大學 Portal 申請
    CLIENT_SECRET = 'YUustASvU0LWPSFXygagued9EILygcfv4h3xofCYJYAuQEoMXrLatvFy'  # 從中央大學 Portal 申請
    # CLIENT_ID = '20241006124146JNAtIrxu5pib' #AWS
    # CLIENT_SECRET = '6aEUaGj20UIynYA3qp6ezElULErCSuRMYQnseXzqUluoK3NMYT5QfxNk'  #AWS
    AUTHORIZATION_URL = 'https://portal.ncu.edu.tw/oauth2/authorization'
    TOKEN_URL = 'https://portal.ncu.edu.tw/oauth2/token'
    USER_INFO_URL = 'https://portal.ncu.edu.tw/apis/oauth/v1/info'
    # REDIRECT_URI = 'http://localhost:5000/customers/callback'  # 回調 URL
    REDIRECT_URI = 'http://15.152.37.157:5000/customers/callback'  # AWS
    SCOPE = 'id identifier chinese-name email mobile-phone personal-id'

    # Flask-Mail 設定
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ncucampuseats@gmail.com'
    MAIL_PASSWORD = 'lqaykqriqgxmhoxc'  # 要記得填入
    MAIL_DEFAULT_SENDER = 'ncucampuseats@gmail.com'
