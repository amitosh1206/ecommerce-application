from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --- Product Data ---
products = [
    {"id": 1, "name": "Product A", "price": 100},
    {"id": 2, "name": "Product B", "price": 200},
    {"id": 3, "name": "Product C", "price": 300},
]

# --- Database Helper ---
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Home ---
@app.route('/')
def home():
    return render_template('home.html')

# --- Register ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except:
            flash('Username already exists!')
        finally:
            conn.close()
    return render_template('register.html')

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user'] = user['username']
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

# --- Logout ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

# --- Change Password ---
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        current = request.form['current']
        new = request.form['new']
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (session['user'], current)).fetchone()
        if user:
            conn.execute('UPDATE users SET password = ? WHERE username = ?', (new, session['user']))
            conn.commit()
            flash('Password changed successfully.')
        else:
            flash('Current password is incorrect.')
        conn.close()
    return render_template('change_password.html')

# --- Products Page ---
@app.route('/products')
def show_products():
    return render_template('products.html', products=products)

# --- Add to Cart ---
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    return redirect(url_for('show_cart'))

# --- View Cart ---
@app.route('/cart')
def show_cart():
    cart_items = []
    total = 0
    if 'cart' in session:
        for pid in session['cart']:
            for p in products:
                if p['id'] == pid:
                    cart_items.append(p)
                    total += p['price']
    return render_template('cart.html', cart=cart_items, total=total)

if __name__ == '__main__':
    # Automatically create database table if not exist
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)')
    conn.close()
    app.run(debug=True)
