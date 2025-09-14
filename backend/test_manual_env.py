import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env.manual file
load_dotenv('.env.manual')

# Get the Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("Testing with manually created .env.manual file")
print("=============================================")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key}")
print(f"Key length: {len(supabase_key) if supabase_key else 'N/A'}")

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