import requests
import json

# Test the council API endpoints
BASE_URL = "http://localhost:8000"

def test_get_all_councils():
    """Test getting all councils"""
    try:
        response = requests.get(f"{BASE_URL}/supabase/councils")
        print(f"GET /supabase/councils - Status: {response.status_code}")
        if response.status_code == 200:
            councils = response.json()
            print(f"Found {len(councils)} councils")
            for council in councils[:3]:  # Show first 3 councils
                print(f"  - {council['council_name']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def test_get_council_by_id(council_id):
    """Test getting a specific council by ID"""
    try:
        response = requests.get(f"{BASE_URL}/supabase/councils/{council_id}")
        print(f"GET /supabase/councils/{council_id} - Status: {response.status_code}")
        if response.status_code == 200:
            council = response.json()
            print(f"  Name: {council['council_name']}")
            print(f"  Domain: {council['domain_description']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    print("Testing Council API Endpoints")
    print("=" * 40)
    
    # Test getting all councils
    test_get_all_councils()
    
    print()
    
    # Test getting a specific council
    test_get_council_by_id("council_digital_identity")