from flask import Flask, jsonify, request, make_response, render_template, redirect, url_for, session
from faker import Faker
import uuid
from functools import wraps  # 添加这行
import json
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 添加这行来设置 session 密钥
fake = Faker('zh_CN')

# 是否开启认证
open_auth = True

# 生成随机用户数据
def generate_random_data():
    return {
        'email': fake.email(),
        'password': fake.password(),
        'username': fake.user_name(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'city': fake.city(),
        'state': fake.province(),
        'zip': fake.postcode(),
        'country': '中国'
    }
    
# 生成随机订单
def generate_random_order():
    return {
        'id': fake.random_int(min=1, max=100),
        'user_id': fake.random_int(min=1, max=100),
        'product_id': fake.random_int(min=1, max=100),
        'amount': fake.random_int(min=1, max=100),
        'status': fake.random_element(elements=('pending', 'shipped', 'delivered', 'cancelled')),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'city': fake.city(),
    }

# 新增生成随机数据的函数
def generate_product_name():
    adjectives = ['高级', '豪华', '时尚', '经典', '创新', '智能', '便携', '多功能']
    nouns = ['手机', '电脑', '相机', '手表', '耳机', '音箱', '平板', '电视', '冰箱', '洗衣机', '空调', '微波炉', '电饭煲', 'T恤', '牛仔裤', '连衣裙', '外套', '西装', '白菜', '番茄', '黄瓜', '胡萝卜', '苹果', '香蕉', '橙子', '葡萄', '面包', '牛奶', '饼干', '巧克力', '感冒药', '消炎药', '维生素', '退烧药', '电视机', '洗碗机', '吸尘器', '电熨斗', '电水壶', '咖啡机', '吹风机', '电动牙刷', '剃须刀', '裙子', '衬衫', '夹克', '毛衣', '短裤', '袜子', '内衣', '茄子', '土豆', '青椒', '豆角', '西瓜', '草莓', '樱桃', '梨', '火腿', '奶酪', '酸奶', '果汁', '止痛药', '抗生素', '胃药', '眼药水', '空气净化器', '加湿器', '电风扇', '电烤箱']
    return f"{random.choice(adjectives)}{random.choice(nouns)}"

def generate_random_product():
    categories = ['电子产品', '服装', '食品', '家居', '美妆', '图书', '运动', '玩具']
    return {
        'id': fake.random_int(min=1, max=100),
        'name': generate_product_name(),  # 使用新的函数
        'price': fake.random_int(min=0, max=100000),
        'stock': fake.random_int(min=0, max=1000),
        'category': fake.random_element(elements=categories),
        'discount': round(random.uniform(0.1, 1.0), 2)  # 添加折扣字段
    }

def generate_random_supplier():
    return {
        'id': fake.random_int(min=1, max=100),
        'name': fake.company(),
        'contact': fake.name(),
        'phone': fake.phone_number(),
        'address': f"{fake.province()} {fake.city()} {fake.street_address()}"
    }

def generate_random_coupon():
    return {
        'id': fake.random_int(min=1, max=100),
        'code': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
        'discount': round(fake.random.uniform(0.1, 0.5), 2),
        'valid_until': (datetime.now() + timedelta(days=fake.random_int(min=1, max=90))).strftime('%Y-%m-%d')
    }

def generate_random_address():
    return {
        'id': fake.random_int(min=1, max=100),
        'user_id': fake.random_int(min=1, max=100),
        'recipient': fake.name(),
        'phone': fake.phone_number(),
        'province': fake.province(),
        'city': fake.city(),
        'district': fake.district(),
        'detail': fake.street_address()
    }

def generate_random_role():
    roles = ['管理员', '普通用户', '编辑', '审核员', '客服', '财务', '运营', '技术支持']
    return {
        'id': fake.random_int(min=1, max=10),
        'name': fake.random_element(elements=roles),
        'description': fake.sentence(nb_words=6, variable_nb_words=True)
    }

def generate_random_menu():
    menu_items = [
        ('用户管理', 'el-icon-user'),
        ('商品管理', 'el-icon-goods'),
        ('订单管理', 'el-icon-s-order'),
        ('仪表盘', 'el-icon-s-data'),
        ('系统设置', 'el-icon-setting'),
        ('优惠券管理', 'el-icon-discount'),
        ('地址管理', 'el-icon-location'),
        ('角色管理', 'el-icon-role'),
        ('菜单管理', 'el-icon-menu'),
    ]
    menu_item = fake.random_element(elements=menu_items)
    return {
        'id': fake.random_int(min=1, max=10),
        'name': menu_item[0],
        'url': f'/{"-".join(menu_item[0].lower().split())}',
        'icon': menu_item[1]
    }

def print_request_info():
    print(f"请求方法: {request.method}")
    print(f"请求URL: {request.url}")
    print(f"请求头: {json.dumps(dict(request.headers), indent=2, ensure_ascii=False)}")
    print(f"请求参数: {json.dumps(request.args.to_dict(), indent=2, ensure_ascii=False)}")
    if request.is_json:
        print(f"请求体: {json.dumps(request.json, indent=2, ensure_ascii=False)}")
    elif request.form:
        print(f"表单数据: {json.dumps(request.form.to_dict(), indent=2, ensure_ascii=False)}")
    print("---")

@app.before_request
def log_request_info():
    print_request_info()

@app.after_request
def set_cookie(response):
    if response.status_code == 200 and 'Cookie' not in request.headers and 'Authorization' not in request.headers:
        response.set_cookie('session_id', fake.uuid4())
    return response

# 添加一个装饰器来检查cookie
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        
        if open_auth is True:
            # 检查session_id是否存在,注释既不检查
            if not session_id or session.get('user_id') != session_id:
                return jsonify({"error": "未授权访问"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/user', methods=['POST'])
@require_auth
def create_user():
    return jsonify({"message": "用户创建成功", "user": generate_random_data()}), 200

@app.route('/api/user/<int:user_id>', methods=['GET'])
@require_auth
def get_user_by_id(user_id):
    # 这里你可以使用user_id来获取特定用户的数据
    # 现在我们仍然返回随机数据，但是添加了user_id
    user_data = generate_random_data()
    user_data['id'] = user_id
    return jsonify(user_data), 200

@app.route('/api/users', methods=['GET'])
@require_auth
def get_users():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    users = [generate_random_data() for _ in range(page_size)]
    return jsonify({
        "users": users,
        "total": 100,
        "page": page,
        "page_size": page_size
    }), 200

@app.route('/api/sensitive_data', methods=['GET'])
@require_auth
def get_sensitive_data():
    return jsonify({
        "name": fake.user_name(),
        "ip": fake.ipv4(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "email": fake.email(),
        "bank_account": fake.credit_card_number(),
        "id_card": fake.ssn(),
        "secret_key": fake.uuid4()
    }), 200

@app.route('/api/user/<int:user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    return jsonify({"message": f"用户 {user_id} 已被删除"}), 200


# 查询用户订单 GET order_id 
@app.route('/api/order/<int:order_id>', methods=['GET'])
@require_auth
def get_order_by_id(order_id):
    # 这里你可以使用order_id来获取特定订单的数据
    # 现在我们仍然返回随机数据，但是添加了order_id
    order_data = generate_random_order()
    order_data['id'] = order_id
    return jsonify(order_data), 200

# 查询全部订单 GET orders_id page_size number
@app.route('/api/orders', methods=['GET'])
@require_auth
def get_orders():   
    page_size = int(request.args.get('page_size', 10))
    number = int(request.args.get('number', 10))
    orders = [generate_random_order() for _ in range(page_size)]
    return jsonify({
        "orders": orders,
        "total": 100,
        "page_size": page_size,
        "number": number
    }), 200

@app.route('/api/user_info', methods=['GET'])
@require_auth
def get_user_info():
    session_id = request.cookies.get('session_id')
    if session_id and session.get('user_id') == session_id:
        # 这里我们生成一些随机的用户信息
        user_info = {
            'username': fake.user_name(),
            'email': fake.email(),
            'role': 'admin'  # 您可以根据需要设置不同的角色
        }
        return jsonify(user_info), 200
    else:
        return jsonify({"error": "未授权访问"}), 401

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session_id = str(uuid.uuid4())
            session['user_id'] = session_id  # 在服务器端存储 session
            response = make_response(redirect(url_for('index')))
            response.set_cookie('session_id', session_id, httponly=True)
            return response
        else:
            return jsonify({"message": "登录失败"}), 401
    return render_template('login.html')

@app.route('/')
def index():
    session_id = request.cookies.get('session_id')
    if session_id:
        # 用户信息
        user_info = {
            'username': fake.user_name(),
            'email': fake.email(),
            'role': 'admin'
        }
        # 仪表盘数据
        dashboard_data = {
            'total_users': fake.random_int(min=1000, max=10000),
            'total_orders': fake.random_int(min=5000, max=50000),
            'total_revenue': round(fake.random.uniform(100000, 1000000), 2),
            'new_users_today': fake.random_int(min=10, max=100)
        }
        return render_template('index.html', userInfo=user_info, dashboardData=dashboard_data)
    return redirect(url_for('login'))

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)  # 从服务器端移除 session
#     response = make_response(redirect(url_for('login')))
#     response.delete_cookie('session_id')
#     return response

# 新增API路由
@app.route('/api/dashboard', methods=['GET'])
@require_auth
def get_dashboard_data():
    return jsonify({
        'total_users': fake.random_int(min=1000, max=10000),
        'total_orders': fake.random_int(min=5000, max=50000),
        'total_revenue': round(fake.random.uniform(100000, 1000000), 2),
        'new_users_today': fake.random_int(min=10, max=100)
    }), 200

@app.route('/api/products', methods=['GET'])
@require_auth
def get_products():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    products = [generate_random_product() for _ in range(page_size)]
    return jsonify({
        "products": products,
        "total": 100,
        "page": page,
        "page_size": page_size
    }), 200

@app.route('/api/suppliers', methods=['GET'])
@require_auth
def get_suppliers():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    suppliers = [generate_random_supplier() for _ in range(page_size)]
    return jsonify({
        "suppliers": suppliers,
        "total": 100,
        "page": page,
        "page_size": page_size
    }), 200

@app.route('/api/coupons', methods=['GET'])
@require_auth
def get_coupons():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    coupons = [generate_random_coupon() for _ in range(page_size)]
    return jsonify({
        "coupons": coupons,
        "total": 100,
        "page": page,
        "page_size": page_size
    }), 200

@app.route('/api/addresses', methods=['GET'])
@require_auth
def get_addresses():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    addresses = [generate_random_address() for _ in range(page_size)]
    return jsonify({
        "addresses": addresses,
        "total": 100,
        "page": page,
        "page_size": page_size
    }), 200

@app.route('/api/roles', methods=['GET'])
@require_auth
def get_roles():
    roles = [generate_random_role() for _ in range(10)]
    return jsonify({"roles": roles}), 200

@app.route('/api/menus', methods=['GET'])
@require_auth
def get_menus():
    menus = [generate_random_menu() for _ in range(10)]
    return jsonify({"menus": menus}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # 从服务器端移除 session
    response = make_response(jsonify({"message": "退出成功"}))
    response.delete_cookie('session_id')
    return response, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
