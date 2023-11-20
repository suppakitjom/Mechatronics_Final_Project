import requests
# from mongocode import update_revenue, update_stock, get_price
response = requests.get(url='http://0.0.0.0:6969/clearitems')

# response = requests.post(url='http://0.0.0.0:6969/add',json={"name": "gold"})
print(response.text)

# data = [{"name":"black","price":720,"quantity":6}]
# update_revenue(update_stock(data))
# print(get_price('black'))