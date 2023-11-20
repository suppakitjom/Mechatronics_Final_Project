
# This code is the backend of the application. It contains 3 functions. The first function is clearitems, which will clear the item in the cart. The second function is add_data, which will add the item to the cart. The last function is get_data, which will return the list of items in the cart.


from flask import Flask, jsonify, request
from flask_cors import CORS
from promptpay import qrcode
from mongocode import update_revenue, update_stock, get_price


app = Flask(__name__)
CORS(app)

global data
data = [] # variable to store items in the format of [{"name": name, "price": price, "quantity": quantity}, ...]

def generate_qr(id, amount):
    '''
    Generate QR code from PromptPay id and amount
    '''
    payload = qrcode.generate_payload(id, amount)
    img = qrcode.to_image(payload)
    qrcode.to_file(payload, "src/pages/qrcode.png") 

@app.route('/clearitems', methods=['GET']) 
def clearitems():
    '''
    Clear items in the cart, update revenue and stock on MongoDB
    '''
    global data
    update_revenue(update_stock(data))
    data.clear()
    return jsonify(data)


# lookup_price = {'gold': 80, 'white': 60, 'red': 40,'black':120}

@app.route('/add', methods=['POST'])
def add_data():
    '''
    Add item to the cart, automatically look up price of item
    '''
    # prepare item data to be added to cart
    item = dict(request.json)
    item["price"] = get_price(item["name"])
    item["quantity"] = 1

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
    '''
    Endpoint for web application to get list of items in the cart, automatically updates the qr code
    '''
    global data
    total_price = 0
    for item in data:
        total_price += int(item['price']) * int(item['quantity'])
    generate_qr('0958934433', total_price)
    return jsonify(data)

if __name__ == "__main__":
    generate_qr('0958934433', 0)
    app.run(host='0.0.0.0', port=6969)
