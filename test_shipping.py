# test_shipping.py
import os, json
from dotenv import load_dotenv
from easypost import EasyPostClient

load_dotenv()
client = EasyPostClient(os.getenv("EASYPOST_API_KEY"))

# Accept common aliases returned in test mode
allowed_aliases = {
    "UPS": {"UPS"},  # you'll see this once UPS is connected
    "FedEx": {"FedEx", "FedExDefault"},
    "DHLExpress": {"DHLExpress", "DHL", "DHL Express"},
}
allowed_flat = set().union(*allowed_aliases.values())  # {"UPS","FedEx","FedExDefault","DHLExpress","DHL","DHL Express"}

from_addr = {
    "name": os.getenv("SENDER_NAME"),
    "street1": os.getenv("SENDER_STREET"),
    "city": os.getenv("SENDER_CITY"),
    "state": os.getenv("SENDER_STATE"),
    "zip": os.getenv("SENDER_ZIP"),
    "country": os.getenv("SENDER_COUNTRY"),
    "phone": os.getenv("SENDER_PHONE"),
    "email": os.getenv("SENDER_EMAIL"),
}

to_addr = {
    "name": "Test Receiver",
    "street1": "1 Market St",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94105",
    "country": "US",
    "phone": "415-555-1234",
    "email": "receiver@example.com",
}

parcel_specs = json.loads(os.getenv("PARCEL_SPECS_JSON"))
first = list(parcel_specs.values())[0]  # [L, W, H, OZ]
parcel = {"length": first[0], "width": first[1], "height": first[2], "weight": first[3]}

shipment = client.shipment.create(to_address=to_addr, from_address=from_addr, parcel=parcel)

available = sorted({r["carrier"] for r in shipment.rates})
print("Available carriers from EasyPost:", available)

rates = [r for r in shipment.rates if r["carrier"] in allowed_flat]
if not rates:
    raise SystemExit(f"No allowed rates. Allowed={sorted(allowed_flat)} Got={available}")

best = min(rates, key=lambda r: float(r["rate"]))
print(f"✅ Best Rate: {best['carrier']} {best['service']} ${best['rate']}")
for r in rates:
    print(f"- {r['carrier']} {r['service']} ${r['rate']}")
