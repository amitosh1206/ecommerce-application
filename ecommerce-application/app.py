from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

products = [
    {"id": 1, "name": "Product A", "price": 100},
    {"id": 2, "name": "Product B", "price": 200},
    {"id": 3, "name": "Product C", "price": 300},
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def show_products():
    return render_template('products.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    return redirect(url_for('show_cart'))

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
    app.run(debug=True)
