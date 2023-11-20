import pymongo
from pymongo import MongoClient
conn_str = "mongodb+srv://mechatronics:262A4STw@class.tqoukoo.mongodb.net/"
client = MongoClient(conn_str)

db = client["sushiro"]
inventory_collection = db["inventory"]
revenue_collection = db["revenue"]

def update_revenue(receipt):
    current_revenue = revenue_collection.find_one({"_id": "001"})['balance']
    new_revenue = int(current_revenue) + int(receipt)
    revenue_collection.update_one({"_id": "001"}, {"$set": {"balance": str(new_revenue)}})
    print("Total Balance Updated")

def update_stock(orders):
    receipt = 0
    for order in orders:
        item_name = order['name']
        quantity_ordered = int(order['quantity'])
        current_stock = inventory_collection.find_one({"name": item_name})
        if current_stock:
            unit_price = int(current_stock['unit_price'])
            receipt+= quantity_ordered*unit_price
            new_quantity = int(current_stock['quantity']) - quantity_ordered
            inventory_collection.update_one({"name": item_name}, {"$set": {"quantity": str(new_quantity)}})
        else:
            print(f"Item {item_name} not found in stock.")
    print(f"{receipt} dollars in total")
    return receipt

def get_price(item):
    current_stock = inventory_collection.find_one({"name": item})
    if current_stock:
            unit_price = int(current_stock['unit_price'])
            return unit_price
    return 0