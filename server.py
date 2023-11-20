from flask import Flask, jsonify, request
from flask_cors import CORS
from promptpay import qrcode
from mongocode import update_revenue, update_stock
app = Flask(__name__)
CORS(app)

global data
data = []

def generate_qr(id, amount):
    payload = qrcode.generate_payload(id, amount)
    img = qrcode.to_image(payload)
    qrcode.to_file(payload, "public/qrcode.png") 

@app.route('/clearitems', methods=['GET']) 
def clearitems():
    global data
    update_revenue(update_stock(data))
    data.clear()
    return jsonify(data)


lookup_price = {'gold': 80, 'white': 60, 'red': 40,'black':120}

@app.route('/add', methods=['POST'])
def add_data():
    item = dict(request.json)
    item["price"] = lookup_price[item["name"]]
    item["quantity"] = 1
    # data = [
    #     {"name": "test", "price": "100", "quantity": "1"},
    #     {"name": "test2", "price": "200", "quantity": "2"},
    #     {"name": "test3", "price": "300", "quantity": "3"},
    #     {"name": "test2", "price": "200", "quantity": "2"},
    #     {"name": "test2", "price": "200", "quantity": "2"},
    #     {"name": "test3", "price": "300", "quantity": "3"},
    #     {"name": "test2", "price": "200", "quantity": "2"},
    #     {"name": "test2", "price": "200", "quantity": "2"},
    # ]
    global data
    # if item with same name already exists, increase quantity and price, otherwise add new item

    for i in range(len(data)):
        if data[i]["name"] == item["name"]:
            data[i]["quantity"] += 1
            data[i]["price"] = int(data[i]["price"]) + int(item["price"])
            return jsonify(data)
    data.append(item)
    return jsonify(data)

@app.route('/order', methods=['GET'])
def get_data():
    global data
    total_price = 0
    for item in data:
        total_price += int(item['price']) * int(item['quantity'])
    generate_qr('0958934433', total_price)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)
