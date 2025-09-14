"""
Test script to verify Supabase connection with actual credentials
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    print("Supabase Connection Test")
    print("========================")
    
    # Get Supabase credentials from environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in the .env file")
        return
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key: {supabase_key[:10]}...{supabase_key[-5:]}")
    
    # Check if the key is a service role key (should start with "eyJhbGci" for JWT or "sbp_" for service key)
    if supabase_key.startswith("eyJhbGci"):
        print("⚠️  Warning: This appears to be a JWT token, not a service role key.")
        print("   Some operations may be restricted.")
    elif supabase_key.startswith("sbp_"):
        print("✓ This appears to be a service role key.")
    else:
        print("⚠️  Warning: Unrecognized key format.")
    
    try:
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✓ Supabase client created successfully")
        
        # Test connection by querying the councils table
        print("\nTesting connection by querying councils table...")
        response = supabase.table("councils").select("*").limit(1).execute()
        print("✓ Connection test successful")
        print(f"  - Table exists and is accessible")
        print(f"  - Response type: {type(response)}")
        
        # Test inserting a temporary record
        print("\nTesting data insertion...")
        test_council = {
            "id": "test_council_temp",
            "council_name": "Test Council",
            "domain_description": "Temporary test council for connection verification",
            "revenue_model_description": "Test revenue model",
            "ethical_boundary": "Test ethical boundary",
            "status": "ACTIVE"
        }
        
        insert_response = supabase.table("councils").insert(test_council).execute()
        print("✓ Data insertion test successful")
        
        # Test deleting the temporary record
        print("\nCleaning up test data...")
        delete_response = supabase.table("councils").delete().eq("id", "test_council_temp").execute()
        print("✓ Test data cleanup successful")
        
        print("\n🎉 All Supabase connection tests passed!")
        print("The Supabase integration is working correctly with the actual credentials.")
        
    except Exception as e:
        print(f"✗ Error connecting to Supabase: {e}")
        print("Please check your credentials and network connection.")

if __name__ == "__main__":
    main()