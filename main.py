import os
import sys
from importlib import import_module

# Ensure the directory containing this script is searched first when importing
# modules. This avoids accidentally pulling in similarly named third-party
# packages (for example a pip-installed "shipping" package) which can lead to
# missing attributes like the ``create_shipment`` function used below.
sys.path.insert(0, os.path.dirname(__file__))




def select_market():
    print("Please select a market:")
    markets = ['DH', 'NXS', 'ARG', 'ATL', 'BOP', 'TZN', 'AWAZ', 'ANU', 'PRIME', 'VOR', 'MARS', 'EUPH']
    for idx, market in enumerate(markets, 1):
        print(f"{idx}. {market}")

    choice = int(input("Enter the number for the market: ")) - 1
    if 0 <= choice < len(markets):
        return markets[choice]
    else:
        print("Invalid selection, please try again.")
        return select_market()

def get_order_file(market):
    market_dir = os.path.join('orders', market)
    files = [f for f in os.listdir(market_dir) if f.endswith('.txt')]

    if not files:
        print(f"No order files found in {market_dir}")
        return None

    print("Please select an order file:")
    for idx, filename in enumerate(files, 1):
        print(f"{idx}. {filename}")

    choice = int(input("Enter the number for the order file: ")) - 1
    if 0 <= choice < len(files):
        return os.path.join(market_dir, files[choice])
    else:
        print("Invalid selection, please try again.")
        return get_order_file(market)

def main():
    market = select_market()
    order_file = get_order_file(market)
    if not order_file:
        return

    with open(order_file, 'r') as file:
        order_text = file.read()

    # Import and run the market-specific parser
    parser_module = import_module(f'parsers.{market.lower()}')
    order_data = parser_module.parse_order(order_text)

    # Explicitly store the market
    order_data['market'] = market

#    print("\nParsed order data:")
    print("\nFULL PARSED ORDER DATA:", order_data)
    for key, value in order_data.items():
        print(f"{key}: {value}")

    # Import and run market-specific Shipping
    shipping_module = import_module(f'shipping.{market.lower()}_shipping')
    shipping_details = shipping_module.create_shipment(order_data)
    # Update order_data to include shipping details explicitly
    order_data.update(shipping_details)

    # Import and run the market-specific Excel exporter
    excel_module = import_module(f'excel_exports.{market.lower()}_excel')
    excel_module.append_order_to_excel(order_data)
    # Import and run market-specific PDF exporter
    pdf_module = import_module(f'pdf_exports.{market.lower()}_pdf')
    pdf_module.generate_pdf(order_data)



if __name__ == "__main__":
    main()
