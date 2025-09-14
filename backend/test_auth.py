import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from fastapi.security import HTTPAuthorizationCredentials
from auth import verify_token_and_get_payload, get_jwks

async def test_token_validation():
    """
    Test our token validation logic with a real token
    """
    # This is the new token we got from signing in
    token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IjFwcjFDVWlETEFaYXJhYlkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2tzcnZ0dnFxaWt3amJxenBnYWNzLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJlZWMwODkwNS0wZTIyLTQyYWItOGM0Ni1lMjBlZDViODgwNDUiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzU3NzEyOTAxLCJpYXQiOjE3NTc3MDkzMDEsImVtYWlsIjoidGVzdC11c2VyLTEyM0B0ZXN0LWRvbWFpbi5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoidGVzdC11c2VyLTEyM0B0ZXN0LWRvbWFpbi5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiZWVjMDg5MDUtMGUyMi00MmFiLThjNDYtZTIwZWQ1Yjg4MDQ1In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NTc3MDkzMDF9XSwic2Vzc2lvbl9pZCI6ImYzNzUxZTBhLWVmZmItNGYzOC1iMmVjLWViMmQ2MGYxMDgwMiIsImlzX2Fub255bW91cyI6ZmFsc2V9.TRoEAuEjdtYHsFX66ZbJIKwWYsUqcwPmuBetg8lu6yI"
    
    # Create a mock HTTPAuthorizationCredentials object
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    
    try:
        # First, let's check the JWKS
        print("Checking JWKS...")
        jwks = get_jwks()
        print(f"JWKS: {jwks}")
        
        # Test our token validation function
        print("Testing token validation...")
        payload = await verify_token_and_get_payload(credentials)
        print("Token validation successful!")
        print(f"User ID: {payload.get('sub')}")
        print(f"Email: {payload.get('email')}")
        return True
    except Exception as e:
        print(f"Token validation failed: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(test_token_validation())
    if result:
        print("Authentication test PASSED")
    else:
        print("Authentication test FAILED")