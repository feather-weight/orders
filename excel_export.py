import os
from importlib import import_module
from excel_export import append_order_to_excel


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

    parser_module = import_module(f'parsers.{market.lower()}')
    order_data = parser_module.parse_order(order_text)

    # Add market to order_data explicitly
    order_data['market'] = market

    # Print parsed data
    print("\nParsed order data:")
    for key, value in order_data.items():
        print(f"{key}: {value}")

    # Append order to Excel
    append_order_to_excel(order_data)


if __name__ == "__main__":
    main()
