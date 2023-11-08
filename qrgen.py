from promptpay import qrcode

def generate_qr(id, amount):
    payload = qrcode.generate_payload(id, amount)
    img = qrcode.to_image(payload)
    qrcode.to_file(payload, "qrcode.png") 

generate_qr('0958934433', 100)