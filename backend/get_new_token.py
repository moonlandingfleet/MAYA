import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_new_token():
    """
    Get a new token using the Supabase client library
    """
    try:
        # Initialize Supabase client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")  # anon key
        
        if not url or not key:
            print("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
            return None
            
        print(f"Creating client with URL: {url}")
        supabase: Client = create_client(url, key)
        
        # Sign in as the test user
        print("Signing in as test user...")
        response = supabase.auth.sign_in_with_password({
            "email": "test-user-123@test-domain.com",
            "password": "password123"
        })
        
        # Extract the access token
        access_token = response.session.access_token
        refresh_token = response.session.refresh_token
        
        print("Successfully signed in!")
        print(f"Access token: {access_token}")
        print(f"Refresh token: {refresh_token}")
        print(f"User ID: {response.user.id}")
        print(f"User email: {response.user.email}")
        
        # Try to validate this token
        import jwt
        unverified_payload = jwt.decode(access_token, options={"verify_signature": False})
        print(f"Token payload (unverified): {unverified_payload}")
        
        return access_token
        
    except Exception as e:
        print(f"Error signing in: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    get_new_token()