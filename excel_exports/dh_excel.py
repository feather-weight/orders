import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

EXCEL_FILE = 'orders_dh.xlsx'

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
        'Item Price (XMR)': order_data.get('item_price_xmr'),
        'Item Price (USD)': order_data.get('item_price_usd'),
        'Shipping Cost (XMR)': order_data.get('shipping_price_xmr'),
        'Shipping Cost (USD)': order_data.get('shipping_price_usd'),
        'Total Price (XMR)': order_data.get('total_price_xmr'),
        'Total Price (USD)': order_data.get('total_price_usd'),
        'PGP Fingerprint': order_data.get('pgp_fingerprint'),
        # Explicitly prefix PGP key/messages to force text
        'PGP Key': "'" + order_data.get('pgp_key'),
        'Encrypted Messages': "'" + "\n\n".join(order_data.get('encrypted_messages', [])),
        'Plaintext Messages': "'" + "\n\n".join(order_data.get('plaintext_messages', []))
    }

    # Append or create Excel file
    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        df_new = pd.DataFrame([row_data])
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_updated = pd.DataFrame([row_data])

    # Save DataFrame to Excel without index
    df_updated.to_excel(EXCEL_FILE, index=False)

    # Open file and adjust formatting
    workbook = load_workbook(EXCEL_FILE)
    sheet = workbook.active

    columns_to_wrap = ['PGP Key', 'Encrypted Messages', 'Plaintext Messages']
    col_letters = {cell.value: cell.column_letter for cell in sheet[1]}

    for col_name in columns_to_wrap:
        if col_name in col_letters:
            col_letter = col_letters[col_name]
            for cell in sheet[col_letter]:
                cell.alignment = Alignment(wrap_text=True, vertical='top')

    workbook.save(EXCEL_FILE)
    print(f"Order {order_data.get('order_id')} appended successfully to {EXCEL_FILE} with correct formatting.")
