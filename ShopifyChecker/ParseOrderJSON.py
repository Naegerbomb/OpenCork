import json

def process_orders(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not a valid JSON file.")
        return

    orders = data.get("orders", [])
    if not orders:
        print("No orders found in the provided JSON file.")
        return

    for order in orders:
        print(f"Order ID: {order.get('id', 'N/A')}")
        print(f"Order Number: {order.get('order_number', 'N/A')}")
        print(f"Customer Locale: {order.get('customer_locale', 'N/A')}")
        print(f"Financial Status: {order.get('financial_status', 'N/A')}")
        print(f"Created At: {order.get('created_at', 'N/A')}")
        print(f"Subtotal Price: {order.get('current_subtotal_price', 'N/A')} {order.get('currency', 'N/A')}")
        print(f"Total Price: {order.get('current_total_price', 'N/A')} {order.get('currency', 'N/A')}")
        
        print("\nLine Items:")
        for item in order.get('line_items', []):
            print(f"  - Product Name: {item.get('name', 'N/A')}")
            print(f"    Quantity: {item.get('quantity', 'N/A')}")
            print(f"    Price: {item.get('price', 'N/A')} {item.get('price_set', {}).get('shop_money', {}).get('currency_code', 'N/A')}")
        
        print("\nShipping Address:")
        shipping = order.get('shipping_address')
        if shipping:
            print(f"  Province: {shipping.get('province', 'N/A')}")
            print(f"  Country: {shipping.get('country', 'N/A')}")
        else:
            print("  Shipping Address: Not available")
        
        print("-" * 40)

if __name__ == "__main__":
    file_path = input("Please enter the path to the orders.json file: ")
    process_orders(file_path)
