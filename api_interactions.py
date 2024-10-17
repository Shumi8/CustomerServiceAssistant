import hashlib
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

# Function to fetch order details using external API
def get_order_admin_details(params):
    current_datetime_utc = datetime.utcnow()

    hash_input = ''
    sha = ''
    sha.update(hash_input)
    security_key = sha.hexdigest()

    app_id = "YOUR_APP_ID"
    base_url = "YOUR_API_BASE_URL"

    url = f""
    headers = {
        "appId": app_id,
        "timestamp": formatted_datetime,
        "securityKey": security_key,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.text)


# Function to get products, sum, and images from the API
def get_products_sum_and_matas_image(order_number, email):
    logging.info('Getting Products Sum and Images')

    current_datetime_utc = datetime.utcnow()
    formatted_datetime = current_datetime_utc.strftime('%Y%m%d%H%M%S')

    hash_input = (formatted_datetime + 'SECRET_KEY').encode('utf-8')
    sha = hashlib.sha256()
    sha.update(hash_input)
    security_key = sha.hexdigest()

    app_id = "YOUR_APP_ID"
    base_url = "YOUR_API_BASE_URL"

    url = f""
    headers = {
        "appId": app_id,
        "timestamp": formatted_datetime,
        "securityKey": security_key,
    }

    params = {
        "OrderNumber": order_number,
        "Email": email
    }

    response = requests.get(url, headers=headers, params=params).json()

    products = response['OrderParts'][0]['OrderLines']
    product_details = {}
    
    for i, product in enumerate(products):
        product_details[f'ProductId_{i+1}'] = product['ProductInfo']['ProductId']
        product_details[f'NameLines_{i+1}'] = ' '.join(product['ProductInfo']['NameLines'])
        product_details[f'Price_{i+1}'] = product['PriceInfo']['Price']
    
    return product_details


# Function to fetch images from a user ticket
def get_image_from_user(ticket_id):
    logging.info('Getting User Images')

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'YOUR_API_KEY'
    }

    url = f"https://YOUR_ZENDESK_API.com/api/v2/tickets/{ticket_id}/comments.json"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.text)
