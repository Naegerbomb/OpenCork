import os
import json
import requests
from datetime import datetime, timedelta

def load_config(file_path='ShopSetupConfig.json'):
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

def main():
    try:
        config = load_config()
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        orders = fetch_orders(config, start_date, end_date)
        print("Orders:", json.dumps(orders, indent=2))
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
