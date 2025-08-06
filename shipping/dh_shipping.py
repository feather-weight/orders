import os
from dotenv import load_dotenv
from easypost import EasyPostClient

load_dotenv()
client = EasyPostClient(os.getenv("EASYPOST_API_KEY"))

def create_shipment(order_data):
    shipment = client.shipment.create(
        to_address={
            "name": order_data['customer_name'],
            "street1": order_data['street'],
            "city": order_data['city'],
            "state": order_data['state'],
            "zip": order_data['zip'],
            "country": "US",
        },
        from_address={
            "name": "Your Company Name",
            "street1": "Your Street Address",
            "city": "Your City",
            "state": "Your State",
            "zip": "Your ZIP",
            "country": "US",
        },
        parcel={
            "length": 10,  # Adjust as needed
            "width": 8,
            "height": 4,
            "weight": 15.5,
        }
    )

    lowest_rate = shipment.lowest_rate()
    bought_shipment = client.shipment.buy(shipment.id, rate=lowest_rate)

    shipping_details = {
        "tracking_code": bought_shipment.tracking_code,
        "tracking_url": bought_shipment.tracker.public_url,
        "label_url": bought_shipment.postage_label.label_url,
        "carrier": lowest_rate.carrier,
        "service": lowest_rate.service,
        "rate": lowest_rate.rate,
    }

    print("Shipment created successfully!")
    print(shipping_details)

    return shipping_details
