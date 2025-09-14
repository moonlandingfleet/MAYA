import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_jwt_secret():
    """
    Attempt to get the JWT secret from Supabase project settings
    """
    # Get the Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not service_role_key:
        print("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment variables")
        return None
    
    # Try to get project settings which might include the JWT secret
    # Using the service role key for admin access
    settings_url = f"{supabase_url}/rest/v1/"
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(settings_url, headers=headers)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print("Successfully accessed project settings")
            # Look for JWT secret in response headers or body
            # This is a simplified approach - in reality, you'd need to check the Supabase dashboard
            print("Check your Supabase dashboard under Settings > API for the JWT secret")
            print("The JWT secret is typically labeled as 'JWT Secret' or 'anon key'")
        else:
            print(f"Failed to access project settings. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error accessing project settings: {e}")

if __name__ == "__main__":
    get_jwt_secret()