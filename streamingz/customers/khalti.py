import requests
import json

url = "https://a.khalti.com/api/v2/epayment/initiate/"


def get_khalti(id,name):
    
    payload = json.dumps({
        "return_url": "http://127.0.0.1:8000/process-payment/",
        "website_url": "http://127.0.0.1:8000/",
        "amount": 1000,
        "purchase_order_id": id,
        "purchase_order_name": name,
        "customer_info": {
        "name": "MovieStreamz",
        "email": "test@khalti.com",
        "phone": "9800000001"
        }
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    clean = response.json()
    

    return(clean["payment_url"])

def verify_khalti(pidx):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    payload = json.dumps({
        "pidx": pidx,
    })

    headers = {
        'Authorization': 'Key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  
        clean = response.json()
        
        
        if "status" in clean and clean["status"] == "Completed":
            return True
        else:
            return False
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError:  
        print("Invalid response format. Could not parse JSON.")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    
    return False  
