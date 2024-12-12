import requests
from flask import Blueprint, flash, redirect, request, render_template, url_for, session, current_app
from flask_mail import Mail
from app.Services.Auth_Service import *
from app.Repositories import get_session

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth', static_folder='./static')
mail = Mail(current_app)

# 系統首頁
@auth_bp.route('/')
def index():
    return render_template('auth/login.html')

# 1.1 通用的註冊邏輯
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        icon = request.files.get('icon')

        with get_session() as db_session:
            result = register_user_service(db_session, data, icon)
            if 'error' in result:
                flash(result['error'])
                return render_template('auth/register.html', form_data=request.form)
            else:
                flash(result['success'])
                return redirect(url_for('auth.login'))
                
    return render_template('auth/register.html')

# 1.1+1.2 Portal授權完成後的回調處理
@auth_bp.route('/customers/callback')
def callback():
    code = request.args.get('code')

    if not code:
        return "Authorization code not found.", 400

    # 交換授權碼為 access token
    token_response = requests.post(current_app.config['TOKEN_URL'], data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': current_app.config['REDIRECT_URI'],
        'client_id': current_app.config['CLIENT_ID'],
        'client_secret': current_app.config['CLIENT_SECRET'],
    }, headers={'Accept': 'application/json'})

    token_json = token_response.json()
    if 'access_token' not in token_json:
        return "Failed to get access token.", 400

    access_token = token_json['access_token']

    # 使用 access token 取得使用者資訊
    user_info_response = requests.get(current_app.config['USER_INFO_URL'], headers={
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    })

    user_info = user_info_response.json()
    username = user_info.get('identifier')
    password = encrypt_password(user_info.get('personalId')[-4:])
    role = 1  # 1 表示顧客

    name = user_info.get('chineseName')
    phone = user_info.get('mobilePhone')
    email = user_info.get('email')

    with get_session() as db_session:
        # 查詢該學號是否有在用戶資料表中
        user_exists = get_user(db_session, username)

        # 沒有用戶資料表中 -> 自動新增資料
        if not user_exists:
            add_user(db_session, username, password, role)
            add_customer(db_session, name, phone, email, username)
            customer = get_customer(db_session, username)
        else:
            customer = get_customer(db_session, username)

        # 有在用戶資料表中 -> 登入成功，顯示餐廳清單頁面
        session['username'] = username
        session['role'] = role
        session['customer_id'] = customer['customer_id']
        session['customer_name'] = customer['name']
    
    return redirect(url_for('menus.view_store'))  # 新用戶自動導向顧客菜單頁面

# 1.2 一般登入
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with get_session() as db_session:
            # 驗證用戶
            user = authenticate_user_service(db_session, username, password)
            if user:
                session['username'] = user['username']
                session['role'] = user['role']

                if user['role'] == 1:
                    session['customer_id'] = user['customer_id']
                    session['customer_name'] = user['customer_name']
                    return redirect(url_for('menus.view_store', customer_id=user['customer_id']))
                elif user['role'] == 2:
                    session['restaurant_id'] = user['restaurant_id']
                    session['restaurant_name'] = user['restaurant_name']
                    session['icon'] = user['icon']
                    return redirect(url_for('menus.view_menu', restaurant_id=user['restaurant_id']))
            else:
                flash('帳號或密碼錯誤！')
                return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

# 1.2 portal登入
@auth_bp.route('/NCUlogin', methods=['GET', 'POST'])
def portal_login():
    # Redirect to the portal's OAuth login URL
    return redirect(f"{current_app.config['AUTHORIZATION_URL']}?response_type=code&client_id={current_app.config['CLIENT_ID']}&redirect_uri={current_app.config['REDIRECT_URI']}&scope={current_app.config['SCOPE']}")

# 1.3 登出
@auth_bp.route('/logout')
def logout():
    # 清除用戶的 session
    session.clear()
    return redirect(url_for('auth.login'))

# 1.4 忘記密碼
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        with get_session() as db_session:
            result = reset_password(db_session, username, email)
            if 'error' in result:
                flash(result['error'])
                return render_template('auth/forgot_password.html')
            else:
                flash(result['success'])
                return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')

# 1.4 修改密碼
@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        with get_session() as db_session:
            result = change_password_service(db_session, session['username'], current_password, new_password, confirm_password)
            if 'error' in result:
                flash(result['error'],"change_password_error")
                return redirect(url_for('auth.change_password'))
            else:
                flash(result['success'],"change_password_success")
                return redirect(url_for('auth.login'))

    return render_template('auth/change_password.html')

# 1.5抓取原始的個人資料
@auth_bp.route('/view_pf')
def view_pf():
    customer_id = session.get('customer_id')
    customer_name = session.get('customer_name')
    with get_session() as db_session:
        data = get_customer_profile(db_session, customer_id)
        if not data:
            flash("找不到您的資料，請重新登錄", "error")
            return redirect(url_for('auth.login'))
        customer_data = {
            "name": data.name,
            "phone": data.phone,
            "email": data.email
        }
    return render_template('customers/view_customer_pf.html', customer_name=customer_name, customer_pf=customer_data)

# 1.6更新顧客資料
@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    customer_id = session.get('customer_id')
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_phone = request.form.get('phone')
        new_email = request.form.get('email')
        with get_session() as db_session:
            if update_customer_profile(db_session, customer_id, new_name, new_phone, new_email):
                flash("您的個人資料已成功更新！", "edit_profile_success")
            else:
                flash("無法找到您的個人資料，請重新登錄。", "edit_profile_error")
    return redirect(url_for('auth.view_pf'))
