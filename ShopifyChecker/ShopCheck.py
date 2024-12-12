import os
import json
import requests
from datetime import datetime, timedelta, timezone

def load_config(file_path='Ignored Files/ShopSetupConfig.json'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The configuration file '{file_path}' does not exist.")
    with open(file_path, 'r') as file:
        return json.load(file)

def fetch_orders(config, start_date, end_date):
    shop_name = config['shop_name']
    access_token = config['access_token']
    url = f"https://{shop_name}.myshopify.com/admin/api/2023-10/orders.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }
    params = {
        "created_at_min": start_date.isoformat(),
        "created_at_max": end_date.isoformat(),
        "status": "any"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def save_orders_to_file(orders, file_path='Ignored Files/orders.json'):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)

def print_order_ids(orders):
    for order in orders.get('orders', []):
        print(f"Order ID: {order['id']}")

def main():
    try:
        config = load_config()
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=7)
        orders = fetch_orders(config, start_date, end_date)
        save_orders_to_file(orders)
        print_order_ids(orders)
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
