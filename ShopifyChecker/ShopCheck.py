import json
import requests
from datetime import datetime, timedelta

def load_config(file_path='config.json'):
    """Load configuration data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_week_date_range():
    """Calculate the start and end dates of the current week (Monday to Sunday)."""
    today = datetime.utcnow()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return start_of_week, end_of_week

def fetch_orders(config, start_date, end_date):
    """Fetch orders from Shopify within the specified date range."""
    url = f"https://{config['shop_name']}.myshopify.com/admin/api/2023-10/orders.json"
    headers = {
        'X-Shopify-Access-Token': config['api_key'],
        'Content-Type': 'application/json'
    }
    params = {
        'created_at_min': start_date.isoformat() + 'Z',
        'created_at_max': end_date.isoformat() + 'Z',
        'status': 'any'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get('orders', [])

def display_orders(orders):
    """Display basic attributes of the fetched orders."""
    if not orders:
        print("No orders found for the current week.")
        return
    print(f"Found {len(orders)} order(s) placed this week:")
    for order in orders:
        print(f"Order ID: {order['id']}, Total Price: {order['total_price']}, Created At: {order['created_at']}")

def main():
    config = load_config()
    start_date, end_date = get_week_date_range()
    orders = fetch_orders(config, start_date, end_date)
    display_orders(orders)

if __name__ == "__main__":
    main()
