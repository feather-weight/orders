import re
from datetime import datetime

def parse_order(text):
    order = {}

    # Order ID
    order_id_match = re.search(r'Order (\w+)', text)
    order['order_id'] = order_id_match.group(1) if order_id_match else None

    # Paid date
    paid_date_match = re.search(r'Paid on: ([\d\- :]+)', text)
    if paid_date_match:
        order['paid_date'] = paid_date_match.group(1)
        order['date_formatted'] = datetime.strptime(order['paid_date'], '%Y-%m-%d %H:%M:%S').strftime('%d%m%Y')

    # Customer username
    customer_match = re.search(r'Customer: (\w+)', text)
    order['customer_username'] = customer_match.group(1) if customer_match else None

    # Listing
    listing_match = re.search(r'Listing: (.+)', text)
    order['listing'] = listing_match.group(1).strip() if listing_match else None

    # Quantity
    quantity_match = re.search(r'Quantity: (.+)', text)
    order['quantity'] = quantity_match.group(1).strip() if quantity_match else None

    # Shipping method
    shipping_method_match = re.search(r'Shipping: (.+?) XMR', text)
    order['shipping_method'] = shipping_method_match.group(1).strip() if shipping_method_match else None

    # Item price (XMR & USD)
    item_price_match = re.search(r'Ordered items: XMR ([\d\.]+) \| USD ([\d\.]+)', text)
    order['item_price_xmr'] = float(item_price_match.group(1)) if item_price_match else None
    order['item_price_usd'] = float(item_price_match.group(2)) if item_price_match else None

    # Shipping cost (XMR & USD)
    shipping_price_match = re.search(r'Shipping: .+ XMR ([\d\.]+) \| USD ([\d\.]+)', text)
    order['shipping_price_xmr'] = float(shipping_price_match.group(1)) if shipping_price_match else None
    order['shipping_price_usd'] = float(shipping_price_match.group(2)) if shipping_price_match else None

    # Order total (XMR & USD)
    order_total_match = re.search(r'Order total: XMR ([\d\.]+) \| USD ([\d\.]+)', text)
    order['total_price_xmr'] = float(order_total_match.group(1)) if order_total_match else None
    order['total_price_usd'] = float(order_total_match.group(2)) if order_total_match else None

    # Address
    address_match = re.search(r'Address:\n(.+?)\n(.+?)\n(.+)', text, re.MULTILINE)
    if address_match:
        order['customer_name'] = address_match.group(1).strip()
        order['street'] = address_match.group(2).strip()
        city_state_zip = address_match.group(3).strip()
        city_state_zip_match = re.match(r'(.+?) ([A-Z]{2}) (\d{5}(?:-\d{4})?)', city_state_zip)
        if city_state_zip_match:
            order['city'] = city_state_zip_match.group(1).strip()
            order['state'] = city_state_zip_match.group(2)
            order['zip'] = city_state_zip_match.group(3)

    # PGP fingerprint
    fingerprint_match = re.search(r'Key fingerprint: ([A-F0-9]+)', text)
    order['pgp_fingerprint'] = fingerprint_match.group(1) if fingerprint_match else None

    # PGP public key
    pgp_key_match = re.search(r'(-----BEGIN PGP PUBLIC KEY BLOCK-----.*?-----END PGP PUBLIC KEY BLOCK-----)', text, re.DOTALL)
    order['pgp_key'] = pgp_key_match.group(1).strip() if pgp_key_match else None

    # Encrypted messages
    encrypted_messages = re.findall(r'(-----BEGIN PGP MESSAGE-----.*?-----END PGP MESSAGE-----)', text, re.DOTALL)
    order['encrypted_messages'] = encrypted_messages

    # Plaintext messages
    plaintext_messages = re.findall(r'System Generic Plaintext\n(.+?)\n\d{4}-\d{2}-\d{2}', text, re.DOTALL)
    order['plaintext_messages'] = [msg.strip() for msg in plaintext_messages]

    return order
