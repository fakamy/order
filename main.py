from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import init_db, add_order, get_orders, update_order_status, get_order
from datetime import datetime
import os

app = Flask(__name__)

# Initialize the database
init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    order_id = add_order(data['item'], data['name'], data['phone'],
                         data['location'])
    return jsonify({"success": True, "order_id": order_id})


@app.route('/barista')
def barista():
    return render_template('barista.html')


@app.route('/get_orders')
def get_all_orders():
    orders = get_orders(
        include_completed=True)  # Modify this function in database.py
    return jsonify(orders)


@app.route('/complete_order/<int:order_id>', methods=['POST'])
def complete_order(order_id):
    completion_time = datetime.now().isoformat()
    update_order_status(order_id, 'completed', completion_time)
    return jsonify({"success": True})


@app.route('/order_status/<int:order_id>')
def order_status(order_id):
    order = get_order(
        order_id)  # You'll need to implement this function in database.py
    return render_template('order_status.html', order=order)


@app.route('/get_order_status/<int:order_id>')
def get_order_status(order_id):
    order = get_order(order_id)  # This returns a dictionary
    if order:
        return jsonify({"status": order["status"]})
    else:
        return jsonify({"error": "Order not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
