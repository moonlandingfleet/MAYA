import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Get the Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("Supabase Connection Test")
print("=======================")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key}")

# Check for hidden characters
print(f"Key representation: {repr(supabase_key)}")
print(f"Key length: {len(supabase_key)}")

# Check if key starts and ends correctly
if supabase_key.startswith('sbp_'):
    print("✓ Key starts with 'sbp_'")
else:
    print("✗ Key does not start with 'sbp_'")

if len(supabase_key) == 44:
    print("✓ Key has correct length (44 characters)")
else:
    print(f"✗ Key has incorrect length: {len(supabase_key)}")

# Try to initialize Supabase client
try:
    print("Initializing Supabase client...")
    supabase: Client = create_client(supabase_url, supabase_key)
    print("✓ Supabase client initialized successfully")
except Exception as e:
    print(f"✗ Error initializing Supabase client: {e}")
    print(f"Error type: {type(e)}")