import hmac
import hashlib
import base64

def generate_signature(message, secret):
    # Create the HMAC SHA256 signature
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    
    # Encode the signature in Base64
    signature_base64 = base64.b64encode(signature).decode()
    
    return signature_base64

# Example usage
message = "total_amount=1000,transaction_uuid=55-1A-44-5B-5F,product_code=EPAYTEST"
secret = "8gBm/:&EnhH.1/q"
signature = generate_signature(message, secret)
print(signature)
