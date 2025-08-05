import os
from dotenv import load_dotenv
from easypost import EasyPostClient

load_dotenv()

# Initialize EasyPost Client with API key
client = EasyPostClient(os.getenv("EASYPOST_API_KEY"))

# Create shipment via EasyPostClient
shipment = client.shipment.create(
    to_address={
        "name": "Test Recipient",
        "street1": "123 Test St",
        "city": "Test City",
        "state": "CA",
        "zip": "94104",
        "country": "US"
    },
    from_address={
        "name": "Test Sender",
        "street1": "456 Sender St",
        "city": "Sender City",
        "state": "CA",
        "zip": "94107",
        "country": "US"
    },
    parcel={
        "length": 10,
        "width": 8,
        "height": 4,
        "weight": 15.5
    }
)

# Print shipment details and rates
print("Shipment Created Successfully:")
for rate in shipment.rates:
    print(f"{rate.carrier} {rate.service} rate: ${rate.rate}")
