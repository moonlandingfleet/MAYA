"""
Test script to verify the new strategic endpoints for the digital kingdom
"""

import requests
import json
from datetime import datetime

# Test the strategic endpoints
BASE_URL = "http://localhost:8000"

def test_strategic_proposals():
    """Test the strategic proposals endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/strategic/proposals/king_review")
        print(f"GET /strategic/proposals/king_review - Status: {response.status_code}")
        if response.status_code == 200:
            proposals = response.json()
            print(f"Found {len(proposals)} strategic proposals")
            if proposals:
                print("First proposal strategic summary:")
                proposal = proposals[0]
                print(f"  Council: {proposal.get('council_name', 'N/A')}")
                print(f"  Purpose: {proposal.get('proposal_purpose', 'N/A')}")
                print(f"  Strategic Priority: {proposal.get('strategic_priority', 'N/A')}")
                print(f"  Recommendation: {proposal.get('recommendation', 'N/A')}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def test_councils_overview():
    """Test the councils strategic overview endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/strategic/councils/strategic_overview")
        print(f"GET /strategic/councils/strategic_overview - Status: {response.status_code}")
        if response.status_code == 200:
            councils = response.json()
            print(f"Found {len(councils)} councils in strategic overview")
            if councils:
                print("First council overview:")
                council = councils[0]
                print(f"  Name: {council.get('council_name', 'N/A')}")
                print(f"  Role: {council.get('role', 'N/A')}")
                print(f"  Active Proposals: {council.get('active_proposals_count', 'N/A')}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def test_kingdom_dashboard():
    """Test the kingdom dashboard endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/kingdom/dashboard")
        print(f"GET /kingdom/dashboard - Status: {response.status_code}")
        if response.status_code == 200:
            dashboard = response.json()
            print("Kingdom Dashboard:")
            status = dashboard.get('kingdom_status', {})
            print(f"  Total Councils: {status.get('total_councils', 'N/A')}")
            print(f"  Active Councils: {status.get('active_councils', 'N/A')}")
            print(f"  Active Proposals: {status.get('active_proposals', 'N/A')}")
            print(f"  Overall Health: {status.get('overall_health', 'N/A')}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def test_supabase_endpoints():
    """Test the basic Supabase endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/supabase/councils")
        print(f"GET /supabase/councils - Status: {response.status_code}")
        if response.status_code == 200:
            councils = response.json()
            print(f"Found {len(councils)} councils in Supabase")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    print("Testing Strategic Endpoints for Digital Kingdom")
    print("=" * 50)
    print("Make sure the MAYA Core server is running on http://localhost:8000")
    print()
    
    # Test basic Supabase endpoints
    print("1. Testing basic Supabase endpoints...")
    test_supabase_endpoints()
    
    print()
    
    # Test strategic proposals
    print("2. Testing strategic proposals endpoint...")
    test_strategic_proposals()
    
    print()
    
    # Test councils overview
    print("3. Testing councils strategic overview endpoint...")
    test_councils_overview()
    
    print()
    
    # Test kingdom dashboard
    print("4. Testing kingdom dashboard endpoint...")
    test_kingdom_dashboard()
    
    print()
    print("Strategic endpoint tests completed!")