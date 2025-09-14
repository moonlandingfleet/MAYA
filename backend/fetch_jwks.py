import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
SUPABASE_JWKS_URI = os.getenv("SUPABASE_JWKS_URI")

print("Fetching Supabase JWKS")
print("======================")
print(f"JWKS URI: {SUPABASE_JWKS_URI}")

try:
    # Fetch the JWKS
    response = requests.get(SUPABASE_JWKS_URI)
    if response.status_code == 200:
        jwks = response.json()
        print("✅ JWKS fetched successfully")
        print(f"Keys available: {len(jwks.get('keys', []))}")
        
        # Print the first key for reference
        if jwks.get('keys'):
            first_key = jwks['keys'][0]
            print(f"First key ID: {first_key.get('kid', 'N/A')}")
            print(f"First key type: {first_key.get('kty', 'N/A')}")
    else:
        print(f"❌ Failed to fetch JWKS: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error fetching JWKS: {e}")