import requests
import uuid
import hmac
import hashlib
import base64


def generate_transaction_uuid():
    return str(uuid.uuid4())


def generate_signature(message, secret):
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def send_esewa_payment(total_amount, transaction_uuid):
    secret = "8gBm/:&EnhH.1/q"  
    
    
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code=EPAYTEST"
    signature = generate_signature(message, secret)

    
    payload = {
        "amount": total_amount,
        "tax_amount": 0,
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": "EPAYTEST",
        "product_service_charge": 0,
        "product_delivery_charge": 0,
        "tax_amount": 0,
        "success_url": "http://localhost:8000/payment_success/",
        "failure_url": "http://localhost:8000/payment_failed/",
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        "signature": signature,
    }

    
    response = requests.post("https://rc-epay.esewa.com.np/api/epay/main/v2/form", data=payload, allow_redirects=False)
    return response
