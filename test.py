import requests
# from mongocode import update_revenue, update_stock
response = requests.get(url='http://0.0.0.0:6969/clearitems')

# response = requests.post(url='http://0.0.0.0:6969/add',json={"name": "black"})
# print(response.text)

# data = [{"name":"black","price":720,"quantity":6}]
# update_revenue(update_stock(data))