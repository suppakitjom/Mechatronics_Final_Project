from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_qr_code():
    pass



@app.route('/order', methods=['GET'])
def get_data():
    data = [
        {"name": "test", "price": "100", "quantity": "1"},
        {"name": "test2", "price": "200", "quantity": "2"},
        {"name": "test3", "price": "300", "quantity": "3"},
        {"name": "test2", "price": "200", "quantity": "2"},
        {"name": "test2", "price": "200", "quantity": "2"},
        {"name": "test3", "price": "300", "quantity": "3"},
        {"name": "test2", "price": "200", "quantity": "2"},
        {"name": "test2", "price": "200", "quantity": "2"},
    ]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)
