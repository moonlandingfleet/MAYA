import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client

def test_supabase_connection():
    """Test Supabase connection with detailed diagnostics"""
    
    print("Supabase Connection Diagnostic")
    print("=============================")
    
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    print(f"1. Environment Variables:")
    print(f"   SUPABASE_URL: {supabase_url}")
    print(f"   SUPABASE_KEY: {'*' * len(supabase_key) if supabase_key else 'NOT SET'}")
    print(f"   Key length: {len(supabase_key) if supabase_key else 'N/A'}")
    
    # Check if variables are set
    if not supabase_url or not supabase_key:
        print("❌ ERROR: Supabase credentials not found in environment variables")
        print("   Please ensure .env file exists with SUPABASE_URL and SUPABASE_KEY")
        return False
    
    # Validate key format
    print(f"\n2. Key Format Validation:")
    if supabase_key.startswith('sbp_') and len(supabase_key) == 44:
        print("   ✅ Service role key format appears correct")
    elif supabase_key.startswith('sb_secret_'):
        print("   ✅ Secret key format detected")
    elif supabase_key.startswith('eyJ'):
        print("   ✅ JWT token format detected")
    else:
        print("   ⚠️  Key format is unexpected")
    
    # Test client initialization
    print(f"\n3. Client Initialization:")
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        print("   ✅ Supabase client initialized successfully")
    except Exception as e:
        print(f"   ❌ Client initialization failed: {e}")
        return False
    
    # Test basic connectivity
    print(f"\n4. Connectivity Test:")
    try:
        # Try to get table names (requires authenticated access)
        response = supabase.table("councils").select("*").limit(1).execute()
        print("   ✅ Successfully connected to Supabase")
        print(f"   ✅ Table 'councils' is accessible")
        print(f"   ✅ Found {len(response.data)} records in test query")
        return True
    except Exception as e:
        print(f"   ❌ Connectivity test failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Additional diagnostics
        if "Invalid API key" in str(e):
            print("   🔍 This suggests the API key is invalid or has insufficient permissions")
        elif "Connection refused" in str(e):
            print("   🔍 This suggests network connectivity issues")
        elif "timeout" in str(e).lower():
            print("   🔍 This suggests network timeout issues")
        
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    
    if success:
        print("\n🎉 All tests passed! Supabase connection is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Supabase connection failed. Please check the errors above.")
        print("\nTroubleshooting steps:")
        print("1. Verify your SUPABASE_URL and SUPABASE_KEY in the .env file")
        print("2. Check that you're using the correct service role key from Supabase dashboard")
        print("3. Ensure your Supabase project is active and not paused")
        print("4. Check your network connectivity")
        sys.exit(1)