import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("Supabase Key Validation")
print("======================")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key}")

# Validate key format
if supabase_key.startswith('sbp_') and len(supabase_key) == 44:
    print("✓ Key format appears correct for service role key")
elif supabase_key.startswith('sb_secret_') and len(supabase_key) == 41:
    print("✓ Key format appears correct for secret key")
elif supabase_key.startswith('eyJ') and len(supabase_key) > 50:
    print("✓ Key format appears correct for JWT token")
else:
    print("✗ Key format is unexpected")

# Try to validate the key by making a direct API call
try:
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}'
    }
    
    # Try to get tables (requires authenticated access)
    response = requests.get(
        f"{supabase_url}/rest/v1/",
        headers=headers
    )
    
    print(f"Direct API call status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Direct API call successful")
    elif response.status_code == 401:
        print("✗ Direct API call failed with 401 (Unauthorized)")
        print("This indicates the key is invalid or has insufficient permissions")
    else:
        print(f"✗ Direct API call failed with status {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"✗ Error making direct API call: {e}")

# Check if we can access the project settings endpoint
try:
    # This is a public endpoint that should work without auth
    response = requests.get(f"{supabase_url}/rest/v1/")
    print(f"Public endpoint status: {response.status_code}")
except Exception as e:
    print(f"Error accessing public endpoint: {e}")