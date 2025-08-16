# sanity_env_test.py
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

print("=== ENV Sanity Test ===")

# 1. Check API Key
api_key = os.getenv("EASYPOST_API_KEY")
if not api_key or not api_key.startswith("EZTK"):
    print("❌ EASYPOST_API_KEY missing or not a test key.")
else:
    print(f"✅ API Key detected: {api_key[:8]}... (test mode)")

# 2. Check sender fields
required_sender_fields = [
    "SENDER_NAME", "SENDER_STREET", "SENDER_CITY", "SENDER_STATE",
    "SENDER_ZIP", "SENDER_COUNTRY", "SENDER_PHONE", "SENDER_EMAIL"
]
for field in required_sender_fields:
    value = os.getenv(field)
    if not value:
        print(f"❌ Missing sender field: {field}")
    else:
        print(f"✅ {field} = {value}")

# 3. Validate JSON fields
json_fields = ["PARCEL_SPECS_JSON", "RAW_AMOUNTS_JSON"]
for field in json_fields:
    raw_value = os.getenv(field)
    try:
        parsed = json.loads(raw_value)
        print(f"✅ {field} loaded successfully with {len(parsed)} entries.")
    except json.JSONDecodeError as e:
        print(f"❌ {field} has invalid JSON: {e}")

print("=== Test Complete ===")
x