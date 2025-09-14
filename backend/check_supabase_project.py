import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_supabase_project():
    """
    Check Supabase project configuration and JWKS status
    """
    # Get the Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not service_role_key:
        print("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment variables")
        return None
    
    print(f"Supabase Project URL: {supabase_url}")
    
    # Check JWKS endpoint
    jwks_url = f"{supabase_url}/auth/v1/.well-known/jwks.json"
    print(f"JWKS URL: {jwks_url}")
    
    try:
        # Check public JWKS
        response = requests.get(jwks_url)
        print(f"JWKS Public Endpoint Status: {response.status_code}")
        if response.status_code == 200:
            jwks_data = response.json()
            print(f"JWKS Content: {jwks_data}")
            print(f"Number of keys: {len(jwks_data.get('keys', []))}")
        else:
            print(f"Failed to fetch JWKS: {response.text}")
    except Exception as e:
        print(f"Error accessing JWKS: {e}")
    
    # Try to access project settings with service role key
    settings_url = f"{supabase_url}/rest/v1/"
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(settings_url, headers=headers)
        print(f"Project Settings Access Status: {response.status_code}")
        if response.status_code == 200:
            print("Successfully accessed project settings with service role key")
            # Check if we can get any auth-related information
            print("Headers:", dict(response.headers))
        else:
            print(f"Failed to access project settings: {response.text}")
    except Exception as e:
        print(f"Error accessing project settings: {e}")
    
    # Try to get auth config
    auth_config_url = f"{supabase_url}/auth/v1/settings"
    auth_headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}"
    }
    
    try:
        response = requests.get(auth_config_url, headers=auth_headers)
        print(f"Auth Config Status: {response.status_code}")
        if response.status_code == 200:
            print("Successfully accessed auth config")
            print("Auth Config:", response.json())
        else:
            print(f"Failed to access auth config: {response.status_code}")
            print("Response:", response.text[:200] if response.text else "No response")
    except Exception as e:
        print(f"Error accessing auth config: {e}")

if __name__ == "__main__":
    check_supabase_project()