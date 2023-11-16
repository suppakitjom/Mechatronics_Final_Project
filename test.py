import requests

response = requests.get(url='http://0.0.0.0:6969/clearitems')

response = requests.post(url='http://0.0.0.0:6969/add',json={"name": "test", "price": "100", "quantity": "1"})
print(response.text)

