import os

# List of market names
markets = ["DH", "NXS", "ARG", "ATL", "BOP", "TZN",
           "AWAZ", "ANU", "PRIME", "VOR", "MARS", "EUPH"]

# Directories to create
base_directories = ['parsers', 'orders', 'output']

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created folder: {path}")
    else:
        print(f"Folder already exists: {path}")

def setup_folders():
    for base_dir in base_directories:
        create_directory(base_dir)

        # Inside 'orders' and 'output', create market-specific folders
        if base_dir in ['orders', 'output']:
            for market in markets:
                market_path = os.path.join(base_dir, market)
                create_directory(market_path)

    # Inside 'parsers', create placeholder parser scripts
    parsers_path = 'parsers'
    for market in markets:
        parser_file = os.path.join(parsers_path, f"{market.lower()}.py")
        if not os.path.exists(parser_file):
            with open(parser_file, 'w') as f:
                f.write(f"# Parser script for {market}\n\ndef parse_order(text):\n    order_data = {{}}\n    # TODO: Implement parsing logic\n    return order_data\n")
            print(f"Created parser script: {parser_file}")
        else:
            print(f"Parser script already exists: {parser_file}")

if __name__ == "__main__":
    setup_folders()
