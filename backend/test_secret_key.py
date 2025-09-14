import os
from supabase import create_client, Client

# Test with the new secret key format
supabase_url = "https://ksrvtvqqikwjbqzpgacs.supabase.co"
supabase_key = "sb_secret_2LQ2UyuHaHcXGT0izmGlqw_KijIQToQ"

print("Testing New Secret Key Format")
print("=============================")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key}")
print(f"Key length: {len(supabase_key)}")

# Check if key starts with correct prefix
if supabase_key.startswith('sb_secret_'):
    print("Key format appears to be a secret key")
else:
    print("Key format is not a secret key")

try:
    print("Initializing Supabase client...")
    supabase: Client = create_client(supabase_url, supabase_key)
    print("SUCCESS: Supabase client initialized successfully")
    
    # Try a simple operation to verify connection
    print("Testing simple query...")
    response = supabase.table("councils").select("*").limit(1).execute()
    print("SUCCESS: Simple query executed successfully")
    print(f"Response data length: {len(response.data) if response.data else 0}")
    
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e)}")