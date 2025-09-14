import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def signin_test_user():
    """
    Sign in as the test user and get a JWT token
    """
    # Get the Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")  # anon key
    
    if not supabase_url or not supabase_key:
        print("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
        return None
    
    # Sign in as the test user
    signin_url = f"{supabase_url}/auth/v1/token?grant_type=password"
    headers = {
        "apikey": supabase_key,
        "Content-Type": "application/json"
    }
    data = {
        "email": "test-user-123@test-domain.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(signin_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            print("Sign in successful:")
            print(f"Access token: {result.get('access_token')}")
            return result.get('access_token')
        else:
            print(f"Failed to sign in. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error signing in: {e}")
        return None

if __name__ == "__main__":
    signin_test_user()