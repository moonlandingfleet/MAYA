import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Get the Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("Supabase Connection Test with Cleaned Key")
print("========================================")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key}")

# Clean the key by stripping whitespace and special characters
cleaned_key = supabase_key.strip()
print(f"Cleaned key: {repr(cleaned_key)}")

# Try to initialize Supabase client with cleaned key
try:
    print("Initializing Supabase client...")
    supabase: Client = create_client(supabase_url, cleaned_key)
    print("✓ Supabase client initialized successfully")
    
    # Try a simple operation to verify connection
    print("Testing simple query...")
    response = supabase.table("councils").select("*").limit(1).execute()
    print("✓ Simple query successful")
    print(f"Response data length: {len(response.data) if response.data else 0}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"Error type: {type(e)}")
    
    # Let's also try with a completely new client instance
    print("\nTrying alternative client initialization...")
    try:
        # Re-import to ensure fresh client
        from supabase import create_client as new_create_client
        supabase_alt: Client = new_create_client(supabase_url, cleaned_key)
        print("✓ Alternative client initialization successful")
    except Exception as e2:
        print(f"✗ Alternative client initialization also failed: {e2}")