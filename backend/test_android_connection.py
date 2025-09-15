"""
Test script to verify Android app can connect to the backend
This script simulates a simple request that the Android app might make
"""

import requests
import json

# Test the connection to the backend
BASE_URL = "http://localhost:8000"

def test_connection():
    """Test basic connection to the backend"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"GET /docs - Status: {response.status_code}")
        if response.status_code == 200:
            print("Successfully connected to the backend server")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def test_councils_endpoint():
    """Test the councils endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/supabase/councils")
        print(f"GET /supabase/councils - Status: {response.status_code}")
        if response.status_code == 200:
            councils = response.json()
            print(f"Found {len(councils)} councils")
            if councils:
                print("First council:")
                print(f"  Name: {councils[0].get('council_name', 'N/A')}")
                print(f"  Domain: {councils[0].get('domain_description', 'N/A')}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    print("Testing Android App Connection to Backend")
    print("=" * 40)
    
    # Test basic connection
    if not test_connection():
        print("Failed to connect to backend. Is the server running?")
        exit(1)
    
    print()
    
    # Test councils endpoint
    test_councils_endpoint()
    
    print("\nConnection tests completed!")