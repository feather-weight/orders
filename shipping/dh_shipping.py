import os
from dotenv import load_dotenv
from easypost import EasyPostClient

load_dotenv()
client = EasyPostClient(os.getenv("EASYPOST_API_KEY"))

def select_parcel(order_data):
    title = order_data['listing'].lower()
    description = order_data['quantity'].lower()

    # Logic for selecting parcel clearly
    if "30mL" in title or "4g" in description:
        parcel_info = os.getenv('PARCEL_1')
    elif "" in title or "medium" in description:
        parcel_info = os.getenv('PARCEL_MEDIUM')
    elif "medium" in title or "medium" in description:
        parcel_info = os.getenv('PARCEL_MEDIUM')
    elif "medium" in title or "medium" in description:
        parcel_info = os.getenv('PARCEL_MEDIUM')
    elif "medium" in title or "medium" in description:
        parcel_info = os.getenv('PARCEL_MEDIUM')
    elif "medium" in title or "medium" in description:
        parcel_info = os.getenv('PARCEL_MEDIUM')
    elif "medium" in title or "medium" in description:
        parcel_info = os.getenv('PARCEL_MEDIUM')
    elif "medium" in title or "medium" in description:
        parcel_info = os.getenv('PARCEL_MEDIUM')
    elif "medium" in title or "medium" in description:
        parcel_info = os.getenv('PARCEL_MEDIUM')
    else:
        parcel_info = os.getenv('PARCEL_SMALL')

    length, width, height, weight = [float(x) for x in parcel_info.split(',')]

    return {
        "length": length,
        "width": width,
        "height": height,
        "weight": weight,
    }

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
            "name": os.getenv("SENDER_NAME"),
            "street1": os.getenv("SENDER_STREET"),
            "city": os.getenv("SENDER_CITY"),
            "state": os.getenv("SENDER_STATE"),
            "zip": os.getenv("SENDER_ZIP"),
            "country": os.getenv("SENDER_COUNTRY"),
        },
        parcel=select_parcel(order_data)  # dynamically select parcel clearly
    )

    try:
        lowest_rate = shipment.lowest_rate()
        bought_shipment = client.shipment.buy(shipment.id, rate=lowest_rate)
    except Exception as e:
        print("Error clearly retrieving or buying rates:", e)
        return None

    shipping_details = {
        "tracking_code": bought_shipment.tracking_code,
        "tracking_url": bought_shipment.tracker.public_url,
        "label_url": bought_shipment.postage_label.label_url,
        "carrier": lowest_rate.carrier,
        "service": lowest_rate.service,
        "rate": lowest_rate.rate,
    }

    print("Shipment created successfully with dynamic parcel selection!")
    print(shipping_details)

    return shipping_details
