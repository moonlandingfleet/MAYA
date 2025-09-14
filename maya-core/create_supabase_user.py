import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_supabase_user():
    """
    Create a test user through the Supabase Auth API
    """
    # Get the Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")  # anon key
    
    if not supabase_url or not supabase_key:
        print("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
        return None
    
    # Sign up a new user
    signup_url = f"{supabase_url}/auth/v1/signup"
    headers = {
        "apikey": supabase_key,
        "Content-Type": "application/json"
    }
    data = {
        "email": "test-user-123@test-domain.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(signup_url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            print("User created successfully:")
            print(result)
            return result
        else:
            print(f"Failed to create user. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

if __name__ == "__main__":
    create_supabase_user()