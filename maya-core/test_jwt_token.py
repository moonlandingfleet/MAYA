import os
from supabase import create_client, Client

# Test with the JWT token
supabase_url = "https://ksrvtvqqikwjbqzpgacs.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzcnZ0dnFxaWt3amJxenBnYWNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NzYxMzE2MiwiZXhwIjoyMDczMTg5MTYyfQ.bLeD9KLtu4bfVvN7mjlQNOUPnI7JshjMPALYFzn_j_A"

print("Testing JWT Token")
print("================")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key[:10]}...{supabase_key[-10:]}")
print(f"Key length: {len(supabase_key)}")

try:
    print("Initializing Supabase client...")
    supabase: Client = create_client(supabase_url, supabase_key)
    print("SUCCESS: Supabase client initialized successfully")
    
    # Try a simple operation to verify connection
    print("Testing simple query...")
    response = supabase.table("councils").select("*").limit(1).execute()
    print("SUCCESS: Simple query executed successfully")
    print(f"Response data length: {len(response.data) if response.data else 0}")
    
    print("\n🎉 CONNECTION SUCCESSFUL! The JWT token works correctly.")
    
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e)}")