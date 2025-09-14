import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Test with the new key format
supabase_url = "https://ksrvtvqqikwjbqzpgacs.supabase.co"
supabase_key = "sb_secret_2LQ2UyuHaHcXGT0izmGlqw_KijIQToQ"

print("Testing New Key Format")
print("=====================")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key}")

# Try to initialize Supabase client
try:
    print("Initializing Supabase client...")
    supabase: Client = create_client(supabase_url, supabase_key)
    print("✓ Supabase client initialized successfully")
    
    # Try a simple operation
    print("Testing simple query...")
    response = supabase.table("councils").select("*").limit(1).execute()
    print("✓ Simple query successful")
    print(f"Response: {response}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"Error type: {type(e)}")