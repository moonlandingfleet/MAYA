"""
Debug script to verify Supabase connection with detailed error information
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    print("Supabase Connection Debug Test")
    print("==============================")
    
    # Get Supabase credentials from environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in the .env file")
        return
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key: {supabase_key}")
    print(f"Key length: {len(supabase_key)}")
    print(f"Key starts with: {supabase_key[:10]}")
    print(f"Key ends with: {supabase_key[-10:]}")
    
    # Check if the key is a service role key
    if supabase_key.startswith("sbp_"):
        print("✓ This appears to be a service role key.")
    else:
        print("⚠️  Warning: This does not appear to be a service role key.")
        print("   Service role keys should start with 'sbp_'")
    
    try:
        # Initialize Supabase client
        print("\nInitializing Supabase client...")
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✓ Supabase client created successfully")
        
        # Test connection by querying the councils table
        print("\nTesting connection by querying councils table...")
        response = supabase.table("councils").select("*").limit(1).execute()
        print("✓ Connection test successful")
        print(f"  - Table exists and is accessible")
        print(f"  - Response type: {type(response)}")
        
    except Exception as e:
        print(f"✗ Error connecting to Supabase: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        print("\nPlease check your credentials and network connection.")

if __name__ == "__main__":
    main()