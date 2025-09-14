import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_service_role_key():
    """
    Attempt to get the service role key from Supabase
    """
    # Get the Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_KEY")  # anon key
    
    if not supabase_url or not anon_key:
        print("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
        return None
    
    # Try to get project settings which might include the service role key
    # This requires admin access, so it might not work with the anon key
    settings_url = f"{supabase_url}/rest/v1/"
    headers = {
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(settings_url, headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        if response.status_code == 200:
            print("Successfully accessed project settings")
            # The service role key might be in the response or headers
            # but it's unlikely to be exposed for security reasons
        else:
            print(f"Failed to access project settings. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error accessing project settings: {e}")

if __name__ == "__main__":
    get_service_role_key()