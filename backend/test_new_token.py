import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_new_token():
    """
    Test validation of the new token we obtained
    """
    # This is the new token we got from signing in
    token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IjFwcjFDVWlETEFaYXJhYlkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2tzcnZ0dnFxaWt3amJxenBnYWNzLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJlZWMwODkwNS0wZTIyLTQyYWItOGM0Ni1lMjBlZDViODgwNDUiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzU3NzEyNTU4LCJpYXQiOjE3NTc3MDg5NTgsImVtYWlsIjoidGVzdC11c2VyLTEyM0B0ZXN0LWRvbWFpbi5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoidGVzdC11c2VyLTEyM0B0ZXN0LWRvbWFpbi5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiZWVjMDg5MDUtMGUyMi00MmFiLThjNDYtZTIwZWQ1Yjg4MDQ1In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NTc3MDg5NTh9XSwic2Vzc2lvbl9pZCI6IjYxZDJjYjIxLTU5OWQtNDc0YS1iY2RhLWJmYTU2OTBiMGViYiIsImlzX2Fub255bW91cyI6ZmFsc2V9.hah-l0OQ91VbtFOgRq8atau4z3nMywl9lHRIaCDv97E"
    
    # Get the keys from environment
    anon_key = os.getenv("SUPABASE_KEY")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    print("=== NEW TOKEN ANALYSIS ===")
    print("Token header:", jwt.get_unverified_header(token))
    print("Token payload (unverified):", jwt.decode(token, options={"verify_signature": False}))
    
    print("\n=== KEY ANALYSIS ===")
    print("Anon key:", anon_key)
    print("Service role key:", service_role_key)
    
    print("\n=== VALIDATION ATTEMPTS ===")
    
    # Try HS256 with service role key
    print("1. HS256 with service role key:")
    try:
        payload = jwt.decode(token, service_role_key, algorithms=["HS256"], 
                           audience="authenticated", 
                           issuer="https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1")
        print("   SUCCESS!")
        print("   Payload:", payload)
        return True
    except Exception as e:
        print("   FAILED:", e)
    
    # Try HS256 with anon key
    print("2. HS256 with anon key:")
    try:
        payload = jwt.decode(token, anon_key, algorithms=["HS256"], 
                           audience="authenticated", 
                           issuer="https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1")
        print("   SUCCESS!")
        print("   Payload:", payload)
        return True
    except Exception as e:
        print("   FAILED:", e)
    
    print("\nAll validation attempts failed")
    return False

if __name__ == "__main__":
    test_new_token()