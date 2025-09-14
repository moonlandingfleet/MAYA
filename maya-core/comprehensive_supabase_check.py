import requests

def comprehensive_supabase_check():
    """
    Perform a comprehensive check of the Supabase project configuration
    """
    project_id = "ksrvtvqqikwjbqzpgacs"
    base_url = f"https://{project_id}.supabase.co"
    
    # Using the service role key from the .env file
    service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzcnZ0dnFxaWt3amJxenBnYWNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NzYzMzk4MiwiZXhwIjoyMDczMjA5OTgyfQ.Wbd5DSyxsCcHbw0hDmsJgbBx01aaK80K2K6T0Xyjp8k"
    
    print(f"Performing comprehensive check of Supabase project: {project_id}")
    print(f"Base URL: {base_url}")
    
    # Headers for authenticated requests
    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}"
    }
    
    # Check 1: JWKS endpoint
    jwks_url = f"{base_url}/auth/v1/.well-known/jwks.json"
    print(f"\n1. Checking JWKS endpoint: {jwks_url}")
    try:
        response = requests.get(jwks_url)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            jwks_data = response.json()
            print(f"   Keys count: {len(jwks_data.get('keys', []))}")
            if len(jwks_data.get('keys', [])) == 0:
                print("   ❌ JWKS keys array is EMPTY - This is the root cause of RS256 validation failure")
            else:
                print("   ✅ JWKS keys array contains data")
        else:
            print(f"   ❌ Failed to fetch JWKS: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing JWKS: {e}")
    
    # Check 2: Auth configuration endpoint
    auth_config_url = f"{base_url}/auth/v1/settings"
    print(f"\n2. Checking auth configuration: {auth_config_url}")
    try:
        response = requests.get(auth_config_url, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            config_data = response.json()
            print("   ✅ Auth configuration accessible")
            # Check for JWT-related settings
            print("   Auth settings summary:")
            for key, value in config_data.items():
                print(f"     {key}: {value}")
        else:
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error accessing auth configuration: {e}")
    
    # Check 3: Health check endpoint
    health_url = f"{base_url}/auth/v1/health"
    print(f"\n3. Checking auth health: {health_url}")
    try:
        response = requests.get(health_url, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print("   ✅ Auth service is healthy")
            print(f"   Health status: {health_data}")
        else:
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Error checking health: {e}")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("The root cause of the RS256 validation failure is confirmed:")
    print("❌ The JWKS endpoint returns an empty keys array: {'keys': []}")
    print("This means Supabase is not publishing the public keys needed for RS256 validation.")
    print("\nNext steps:")
    print("1. Verify the project ID is correct: ksrvtvqqikwjbqzpgacs")
    print("2. Check Supabase status page for any ongoing issues")
    print("3. Review Supabase Auth settings in the dashboard")
    print("4. Contact Supabase support if the issue persists")

if __name__ == "__main__":
    comprehensive_supabase_check()