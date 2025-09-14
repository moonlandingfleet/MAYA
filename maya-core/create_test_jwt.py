import os
import jwt
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_test_jwt():
    """
    Create a test JWT token that should be accepted by our validation logic
    """
    # Get the Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")  # This is the service role key we need
    
    if not supabase_url or not supabase_key:
        print("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
        return None
    
    # Create a payload that matches what Supabase would generate
    payload = {
        "sub": "364730eb-64f5-4d55-a24a-e81aa69d5c50",  # The user ID we created
        "aud": "authenticated",
        "role": "authenticated",
        "email": "test@example.com",
        "exp": int(time.time()) + 3600,  # Token expires in 1 hour
        "iat": int(time.time()),
        "iss": f"{supabase_url}/auth/v1"
    }
    
    # Create the JWT token using HS256 algorithm (what Supabase uses for service role key)
    try:
        token = jwt.encode(payload, supabase_key, algorithm="HS256")
        return token
    except Exception as e:
        print(f"Error creating JWT: {e}")
        return None

if __name__ == "__main__":
    token = create_test_jwt()
    if token:
        print(f"Generated JWT token for test user:")
        print(token)
    else:
        print("Failed to generate JWT token")