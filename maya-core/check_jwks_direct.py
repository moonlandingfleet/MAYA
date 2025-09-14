import requests

def check_jwks_directly():
    """
    Check the JWKS endpoint directly without relying on environment variables
    """
    project_id = "ksrvtvqqikwjbqzpgacs"
    jwks_url = f"https://{project_id}.supabase.co/auth/v1/.well-known/jwks.json"
    
    print(f"Checking JWKS URL: {jwks_url}")
    
    try:
        response = requests.get(jwks_url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            jwks_data = response.json()
            print(f"JWKS Data: {jwks_data}")
            print(f"Keys count: {len(jwks_data.get('keys', []))}")
            
            if len(jwks_data.get('keys', [])) == 0:
                print("\nCONFIRMED: The JWKS keys array is empty!")
                print("This explains why RS256 validation is failing.")
                print("The Supabase project is not publishing its public keys for RS256 validation.")
            else:
                print("\nThe JWKS keys array contains data. RS256 validation should work.")
        else:
            print(f"Failed to fetch JWKS: {response.text}")
    except Exception as e:
        print(f"Error accessing JWKS: {e}")

if __name__ == "__main__":
    check_jwks_directly()