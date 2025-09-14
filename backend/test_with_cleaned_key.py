
import os
from supabase import create_client, Client

supabase_url = "https://ksrvtvqqikwjbqzpgacs.supabase.co"
supabase_key = "sbp_1920f6dc639d6cd3e5bc33a6a449a4aad17cbfcd"

print("Testing with cleaned key:")
print(f"Key length: {len(supabase_key)}")

try:
    print("Initializing Supabase client...")
    supabase: Client = create_client(supabase_url, supabase_key)
    print("SUCCESS: Supabase client initialized successfully")
except Exception as e:
    print(f"ERROR: {e}")
