import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print("Supabase Auth Test")
print("==================")
print(f"Supabase URL: {SUPABASE_URL}")
print(f"Anon Key: {SUPABASE_ANON_KEY[:10]}...{SUPABASE_ANON_KEY[-10:] if SUPABASE_ANON_KEY else ''}")

# Test user credentials
test_email = "maya_test_user@example.com"
test_password = "maya_test_password_123"

# Sign up a new user
signup_url = f"{SUPABASE_URL}/auth/v1/signup"
headers = {
    "apikey": SUPABASE_ANON_KEY,
    "Content-Type": "application/json"
}
data = {
    "email": test_email,
    "password": test_password
}

print(f"\nSigning up user: {test_email}")

try:
    response = requests.post(signup_url, headers=headers, json=data)
    print(f"Signup response status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ User signed up successfully!")
        print(f"User ID: {result.get('user', {}).get('id')}")
        print(f"Access token: {result.get('access_token', 'Not provided')[:20]}...")
    else:
        print(f"❌ Signup failed: {response.status_code}")
        print(f"Error: {response.text}")
        
        # If signup fails, let's try to sign in with an existing user
        print("\nTrying to sign in instead...")
        signin_url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
        response = requests.post(signin_url, headers=headers, json=data)
        print(f"Signin response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ User signed in successfully!")
            print(f"Access token: {result.get('access_token', 'Not provided')[:20]}...")
            # Save the token to a file for later use
            with open("test_user_token.txt", "w") as f:
                f.write(result.get('access_token', ''))
            print("Token saved to test_user_token.txt")
        else:
            print(f"❌ Signin also failed: {response.status_code}")
            print(f"Error: {response.text}")
            
except Exception as e:
    print(f"❌ Error during auth test: {e}")