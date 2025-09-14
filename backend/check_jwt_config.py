import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_jwt_config():
    """
    Check JWT configuration in Supabase project
    """
    # Get the Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not service_role_key:
        print("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment variables")
        return None
    
    print(f"Supabase Project URL: {supabase_url}")
    
    # Try to get JWT settings
    jwt_settings_url = f"{supabase_url}/auth/v1/settings"
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}"
    }
    
    try:
        response = requests.get(jwt_settings_url, headers=headers)
        print(f"JWT Settings Status: {response.status_code}")
        if response.status_code == 200:
            settings = response.json()
            print("JWT Settings:")
            print(settings)
            # Look for JWT-related settings
            jwt_related_keys = []
            for key, value in settings.items():
                if 'jwt' in key.lower() or 'key' in key.lower() or 'secret' in key.lower():
                    jwt_related_keys.append((key, value))
            
            if jwt_related_keys:
                print("\nJWT-related settings found:")
                for key, value in jwt_related_keys:
                    print(f"  {key}: {value}")
            else:
                print("\nNo obvious JWT-related settings found in the response")
        else:
            print(f"Failed to fetch JWT settings: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error accessing JWT settings: {e}")
    
    # Check if there are any specific JWT endpoints
    print("\nTrying to find JWT-specific endpoints...")
    
    # Try the config endpoint
    config_url = f"{supabase_url}/auth/v1/config"
    try:
        response = requests.get(config_url, headers=headers)
        print(f"Config Endpoint Status: {response.status_code}")
        if response.status_code == 200:
            config = response.json()
            print("Config data retrieved successfully")
            print(config)
        else:
            print(f"Config endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"Error accessing config endpoint: {e}")

if __name__ == "__main__":
    check_jwt_config()