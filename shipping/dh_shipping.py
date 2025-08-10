import json
import logging
import os
import re
from typing import Dict, List, Tuple

from dotenv import load_dotenv

# Optional: if you're calling EasyPost here
try:
    import easypost
except ImportError:
    easypost = None

# ---------- Logging ----------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/shipping.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# ---------- Env ----------
load_dotenv()

EASYPOST_API_KEY = os.getenv("EASYPOST_API_KEY", "")

SENDER = {
    "company": os.getenv("SENDER_COMPANY", "Sick Scents"),
    "name": os.getenv("SENDER_NAME", "Knot Your Average Gifts"),
    "street1": os.getenv("SENDER_STREET", ""),
    "city": os.getenv("SENDER_CITY", ""),
    "state": os.getenv("SENDER_STATE", ""),
    "zip": os.getenv("SENDER_ZIP", ""),
    "country": os.getenv("SENDER_COUNTRY", "US"),
    "phone": os.getenv("SENDER_PHONE", ""),
    "email": os.getenv("SENDER_EMAIL", ""),
}

PARCEL_SPECS_JSON = os.getenv("PARCEL_SPECS_JSON", "{}")
RAW_AMOUNTS_JSON = os.getenv("RAW_AMOUNTS_JSON", "{}")

def _json_env(name: str, raw: str) -> Dict:
    try:
        return json.loads(raw)
    except Exception as e:
        logging.error("ENV_PARSE_ERROR %s %s", name, e)
        return {}

PARCEL_SPECS: Dict[str, List[int]] = _json_env("PARCEL_SPECS_JSON", PARCEL_SPECS_JSON)
RAW_AMOUNTS: Dict[str, str] = _json_env("RAW_AMOUNTS_JSON", RAW_AMOUNTS_JSON)

# ---------- Helpers ----------
GRAM_RE = re.compile(r"\b(\d+)\s*grams?\b", re.IGNORECASE)
ML_RE = re.compile(r"\b(\d+)\s*mL\b", re.IGNORECASE)

def _clean_amount_list(csv_str: str) -> List[str]:
    # fix the known typo "500mL750mL" -> "500mL,750mL"
    fixed = csv_str.replace("500mL750mL", "500mL,750mL")
    # split, strip, drop empties
    items = [x.strip() for x in fixed.split(",")]
    return [x for x in items if x]

def build_amount_to_parcel_map() -> Dict[str, Tuple[int,int,int,int]]:
    """
    Enforces:
      PARCELAMT_1 -> PARCEL_1
      ...
      PARCELAMT_10 -> PARCEL_10
    """
    mapping: Dict[str, Tuple[int,int,int,int]] = {}
    for i in range(1, 11):
        amt_key = f"PARCELAMT_{i}"
        box_key = f"PARCEL_{i}"
        raw_csv = RAW_AMOUNTS.get(amt_key, "")
        if not raw_csv:
            continue
        amounts = _clean_amount_list(raw_csv)
        dims = PARCEL_SPECS.get(box_key)
        if not dims:
            logging.warning("MISSING_PARCEL_SPECS %s", box_key)
            continue
        # ensure 4-tuple
        if len(dims) != 4:
            logging.error("BAD_PARCEL_SPEC %s %s", box_key, dims)
            continue
        for label in amounts:
            mapping[label] = tuple(dims)  # (L, W, H, weight_oz)
    return mapping

AMOUNT_TO_PARCEL = build_amount_to_parcel_map()

def pick_parcel_for_amount(amount_label: str) -> Tuple[int,int,int,int]:
    """
    amount_label examples: "30mL", "1 gram", "128 grams", etc.
    Falls back by normalizing pluralization/spacing.
    """
    label = amount_label.strip()
    if label in AMOUNT_TO_PARCEL:
        return AMOUNT_TO_PARCEL[label]

    # Try a normalized variant (e.g., "1 gram" -> "1 grams")
    m = GRAM_RE.search(label)
    if m:
        grams = int(m.group(1))
        alt = f"{grams} grams"
        if alt in AMOUNT_TO_PARCEL:
            return AMOUNT_TO_PARCEL[alt]
    m = ML_RE.search(label)
    if m:
        mls = int(m.group(1))
        alt = f"{mls}mL"
        if alt in AMOUNT_TO_PARCEL:
            return AMOUNT_TO_PARCEL[alt]

    raise KeyError(f"No parcel mapping for amount '{amount_label}'")

# ---------- EasyPost ----------
def _log_easypost_payload(tag: str, payload: Dict):
    """Write exactly what we send to EasyPost (redact api key)."""
    safe = json.dumps(payload, ensure_ascii=False)
    logging.info("EASYPOST_%s %s", tag.upper(), safe)

def create_label(
    to_address: Dict,
    amount_label: str,
    reference: str = "",
    carrier_accounts: List[str] = None,
    options: Dict = None,
) -> Dict:
    """
    Build parcel from amount_label using env-driven mapping,
    log the payload, hit EasyPost, and return the response dict.
    """
    if easypost is None:
        raise RuntimeError("easypost package not installed")

    if not EASYPOST_API_KEY:
        raise RuntimeError("EASYPOST_API_KEY missing")

    easypost.api_key = EASYPOST_API_KEY

    L, W, H, W_OZ = pick_parcel_for_amount(amount_label)

    parcel = {
        "length": L,
        "width": W,
        "height": H,
        "weight": W_OZ,  # ounces
    }

    shipment_payload = {
        "to_address": to_address,
        "from_address": SENDER,
        "parcel": parcel,
        "reference": reference or "",
    }

    if options:
        shipment_payload["options"] = options
    if carrier_accounts:
        shipment_payload["carrier_accounts"] = carrier_accounts

    # Log exactly what we send
    _log_easypost_payload("CREATE_SHIPMENT", shipment_payload)

    # Create shipment
    shipment = easypost.Shipment.create(**shipment_payload)

    # Log rates snapshot (useful during debugging)
    rates_slim = [
        {
            "id": r.id,
            "carrier": r.carrier,
            "service": r.service,
            "rate": r.rate,
            "currency": r.currency,
            "delivery_days": r.delivery_days,
            "carrier_account_id": getattr(r, "carrier_account_id", None),
        }
        for r in shipment.rates
    ]
    logging.info("EASYPOST_RATES %s", json.dumps(rates_slim))

    # (optional) buy the lowest rate
    # best_rate = shipment.lowest_rate()
    # _log_easypost_payload("BUY", {"rate_id": best_rate.id})
    # shipment = shipment.buy(rate=best_rate)

    # Return a plain dict so the app can render/inspect easily
    return json.loads(shipment.to_json())
