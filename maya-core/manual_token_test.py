import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_manual_validation():
    """
    Manually test JWT validation with different keys
    """
    # This is the token we got from signing in
    token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IjFwcjFDVWlETEFaYXJhYlkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2tzcnZ0dnFxaWt3amJxenBnYWNzLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJlZWMwODkwNS0wZTIyLTQyYWItOGM0Ni1lMjBlZDViODgwNDUiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzU3Njg1MjAzLCJpYXQiOjE3NTc2ODE2MDMsImVtYWlsIjoidGVzdC11c2VyLTEyM0B0ZXN0LWRvbWFpbi5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoidGVzdC11c2VyLTEyM0B0ZXN0LWRvbWFpbi5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiZWVjMDg5MDUtMGUyMi00MmFiLThjNDYtZTIwZWQ1Yjg4MDQ1In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NTc2ODE2MDN9XSwic2Vzc2lvbl9pZCI6IjcyNTg5ZmIxLTI0ODQtNDMxYy1iMzQ4LTRiN2Y1OTZmYWFmOCIsImlzX2Fub255bW91cyI6ZmFsc2V9.NG6FPNtbWS0Ueb44o_g-Hggww16u-g4WrGnA4xon1PY"
    
    # Get the keys from environment
    anon_key = os.getenv("SUPABASE_KEY")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    print("Token header:", jwt.get_unverified_header(token))
    print("Token payload (unverified):", jwt.decode(token, options={"verify_signature": False}))
    
    # Try to validate with anon key
    print("\nTrying to validate with anon key...")
    try:
        payload = jwt.decode(token, anon_key, algorithms=["HS256"], 
                           audience="authenticated", 
                           issuer="https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1")
        print("SUCCESS with anon key!")
        print("Payload:", payload)
        return True
    except Exception as e:
        print("Failed with anon key:", e)
    
    # Try to validate with service role key if it's different
    if service_role_key and service_role_key != "PLACEHOLDER_REPLACE_WITH_SERVICE_ROLE_KEY":
        print("\nTrying to validate with service role key...")
        try:
            payload = jwt.decode(token, service_role_key, algorithms=["HS256"], 
                               audience="authenticated", 
                               issuer="https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1")
            print("SUCCESS with service role key!")
            print("Payload:", payload)
            return True
        except Exception as e:
            print("Failed with service role key:", e)
    
    print("\nAll validation attempts failed")
    return False

if __name__ == "__main__":
    test_manual_validation()