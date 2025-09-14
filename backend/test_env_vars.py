import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Supabase credentials
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("Environment Variables Test")
print("=========================")
print(f"SUPABASE_URL: {supabase_url}")
print(f"SUPABASE_KEY: {supabase_key}")

# Check if variables are loaded
if supabase_url and supabase_key:
    print("✓ Environment variables loaded successfully")
    print(f"URL length: {len(supabase_url)}")
    print(f"Key length: {len(supabase_key)}")
else:
    print("✗ Environment variables not loaded properly")