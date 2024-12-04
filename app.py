from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        db='welcomehome',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Route: Home Page
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('main.html', username=session['username'])
    return redirect(url_for('login'))

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT id, username, password_hash FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()

        connection.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Route: Find Single Item
@app.route('/find_item', methods=['GET', 'POST'])
def find_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    item_locations = None
    if request.method == 'POST':
        item_id = request.form['item_id']
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT locations.name AS location_name 
                FROM items 
                JOIN item_locations ON items.id = item_locations.item_id
                JOIN locations ON item_locations.location_id = locations.id
                WHERE items.id = %s
            """
            cursor.execute(sql, (item_id,))
            item_locations = cursor.fetchall()
        connection.close()

    return render_template('find_item.html', item_locations=item_locations)

# Route: Find Order Items
@app.route('/find_order', methods=['GET', 'POST'])
def find_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    order_items = None
    if request.method == 'POST':
        order_id = request.form['order_id']
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT items.name AS item_name, locations.name AS location_name
                FROM orders
                JOIN order_items ON orders.id = order_items.order_id
                JOIN items ON order_items.item_id = items.id
                JOIN item_locations ON items.id = item_locations.item_id
                JOIN locations ON item_locations.location_id = locations.id
                WHERE orders.id = %s
            """
            cursor.execute(sql, (order_id,))
            order_items = cursor.fetchall()
        connection.close()

    return render_template('find_order.html', order_items=order_items)

if __name__ == '__main__':
    app.run(debug=True)
