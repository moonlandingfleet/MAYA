import os
from dotenv import load_dotenv
from supabase import create_client, Client

def verify_supabase_key():
    """Simple script to verify Supabase key after updating"""
    
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    print("Verifying Supabase Key...")
    print(f"URL: {supabase_url}")
    print(f"Key length: {len(supabase_key) if supabase_key else 'N/A'}")
    
    if not supabase_url or not supabase_key:
        print("❌ Missing credentials")
        return
    
    try:
        # Initialize client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Client initialized")
        
        # Test connectivity
        response = supabase.table("councils").select("*").limit(1).execute()
        print("✅ Connection successful")
        print(f"✅ Found {len(response.data)} records in test query")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_supabase_key()