import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_supabase_token(email, password):
    """
    Obtain a JWT token from Supabase using email and password
    """
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error obtaining token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    # You'll need to replace these with actual test user credentials
    # Make sure to create this user in your Supabase project first
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "testpassword123")
    
    print("Obtaining Supabase token...")
    token = get_supabase_token(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    
    if token:
        print("Successfully obtained token!")
        print(f"Token: {token}")
        print("\nTo test the protected endpoint, use this command:")
        print(f'curl -H "Authorization: Bearer {token}" http://localhost:8000/protected')
    else:
        print("Failed to obtain token")
        print("\nPlease make sure:")
        print("1. The test user exists in your Supabase project")
        print("2. The email and password are correct")
        print("3. The SUPABASE_URL and SUPABASE_ANON_KEY in your .env file are correct")