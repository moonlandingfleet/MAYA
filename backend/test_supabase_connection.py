"""
Test script to verify Supabase connection with actual credentials
"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Get Supabase credentials
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print(f"Supabase URL: {url}")
print(f"Supabase Key: {key[:10]}...{key[-10:] if key else 'None'}")

if not url or not key:
    print("Error: Supabase credentials not found in environment variables")
    exit(1)

try:
    # Initialize Supabase client
    supabase = create_client(url, key)
    print("Successfully initialized Supabase client")
    
    # Test connection by querying the councils table
    response = supabase.table("councils").select("*").limit(1).execute()
    print("Successfully connected to Supabase and queried councils table")
    print(f"Response: {response}")
    
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
    exit(1)

print("Supabase connection test completed successfully")
