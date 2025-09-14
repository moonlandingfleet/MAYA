import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_test_user_token():
    """
    Sign in as the test user and get a JWT token
    """
    try:
        # Initialize Supabase client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")  # anon key
        supabase: Client = create_client(url, key)
        
        # Sign in as the test user
        # Note: This requires the user to exist and have a valid password
        response = supabase.auth.sign_in_with_password({
            "email": "test@example.com",
            "password": "password123"
        })
        
        # Extract the access token
        access_token = response.session.access_token
        return access_token
        
    except Exception as e:
        print(f"Error signing in: {e}")
        return None

if __name__ == "__main__":
    token = get_test_user_token()
    if token:
        print(f"Access token for test user: {token}")
    else:
        print("Failed to get access token")