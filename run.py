# import os
from app import create_app
# from flask_cors import CORS
from flask_mail import Mail

app = create_app()
# app.secret_key = os.urandom(24) 
# CORS(app)

# 初始化 Flask-Mail
mail = Mail(app)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True) #aws
    app.run(debug=True)