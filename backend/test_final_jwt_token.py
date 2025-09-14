import os
from supabase import create_client, Client

# Test with the new JWT token
supabase_url = "https://ksrvtvqqikwjbqzpgacs.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzcnZ0dnFxaWt3amJxenBnYWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc2MzM5ODIsImV4cCI6MjA3MzIwOTk4Mn0.-bI36T8jCKyW8b1n1IFl4yAGZXCd_mqX_r3dma7ytCc"

print("Testing Final JWT Token")
print("======================")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key[:10]}...{supabase_key[-10:]}")
print(f"Key length: {len(supabase_key)}")

# Check the role in the token
import base64
import json

# Decode the JWT payload (middle part of the token)
try:
    payload = supabase_key.split('.')[1]
    # Add padding if needed
    payload += '=' * (4 - len(payload) % 4)
    decoded_payload = base64.urlsafe_b64decode(payload)
    payload_data = json.loads(decoded_payload)
    print(f"Token role: {payload_data.get('role', 'Unknown')}")
    print(f"Token expiration: {payload_data.get('exp', 'Unknown')}")
except Exception as e:
    print(f"Could not decode token: {e}")

try:
    print("Initializing Supabase client...")
    supabase: Client = create_client(supabase_url, supabase_key)
    print("SUCCESS: Supabase client initialized successfully")
    
    # Try a simple operation to verify connection
    print("Testing simple query...")
    response = supabase.table("councils").select("*").limit(1).execute()
    print("SUCCESS: Simple query executed successfully")
    print(f"Response data length: {len(response.data) if response.data else 0}")
    
    print("\n🎉 CONNECTION SUCCESSFUL! The final JWT token works correctly.")
    
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e)}")