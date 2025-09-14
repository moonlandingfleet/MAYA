import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("Creating Supabase client...")
print(f"URL: {SUPABASE_URL}")

try:
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client created successfully")
    
    # Try to create a test user in the auth.users table
    # Note: This is a simplified approach for testing purposes
    test_user = {
        "id": "test-user-123",
        "email": "test@example.com",
        "encrypted_password": "testpassword123",
        "email_confirmed_at": "now()",
        "created_at": "now()",
        "updated_at": "now()"
    }
    
    print("Attempting to create test user...")
    # This might not work directly due to auth table restrictions
    # But let's try to insert into a regular table to verify our connection
    
    # First, let's check if we can access the councils table
    response = supabase.table("councils").select("*").limit(1).execute()
    print("✅ Successfully connected to Supabase database")
    print(f"Found {len(response.data)} councils in the database")
    
except Exception as e:
    print(f"❌ Error: {e}")