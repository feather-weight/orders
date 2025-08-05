import os
import pandas as pd

EXCEL_FILE = 'orders_anu.xlsx'

def append_order_to_excel(order_data):
    row_data = {
        'Order ID': order_data.get('order_id'),
        'Paid Date': order_data.get('paid_date'),
        'Username': order_data.get('customer_username'),
        'Customer Name': order_data.get('customer_name'),
        'Street': order_data.get('street'),
        'City': order_data.get('city'),
        'State': order_data.get('state'),
        'Zip': order_data.get('zip'),
        'Listing': order_data.get('listing'),
        'Quantity': order_data.get('quantity'),
        'Shipping Method': order_data.get('shipping_method'),
        'Order Total USD': order_data.get('order_total_usd'),
        'PGP Fingerprint': order_data.get('pgp_fingerprint'),
        'PGP Key': order_data.get('pgp_key'),
        'Encrypted Messages': "\n\n".join(order_data.get('encrypted_messages', [])),
        'Plaintext Messages': "\n\n".join(order_data.get('plaintext_messages', []))
    }

    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        df_new = pd.DataFrame([row_data])
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_updated = pd.DataFrame([row_data])

    df_updated.to_excel(EXCEL_FILE, index=False)
    print(f"Order {order_data.get('order_id')} appended successfully to {EXCEL_FILE}.")
