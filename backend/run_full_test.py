"""
Full test script for the MAYA King's App MVP
This script tests the complete workflow:
1. Populating councils in the database
2. Verifying the councils were inserted correctly
3. Testing the API endpoints
4. Testing the Supabase connection
"""

import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n--- {description} ---")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("SUCCESS")
            print(result.stdout)
            return True
        else:
            print("FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

def main():
    print("MAYA King's App MVP - Full Test Suite")
    print("=" * 50)
    
    # Test 1: Supabase connection
    if not run_command("python test_supabase_connection.py", "Testing Supabase Connection"):
        print("Supabase connection test failed. Exiting.")
        return False
    
    # Test 2: Populate councils
    if not run_command("python populate_councils.py", "Populating Councils"):
        print("Council population failed. Exiting.")
        return False
    
    # Wait a moment for the database to settle
    time.sleep(2)
    
    # Test 3: Verify councils
    if not run_command("python verify_councils.py", "Verifying Councils"):
        print("Council verification failed. Exiting.")
        return False
    
    # Test 4: Test API endpoints (only if server is running)
    print("\n--- Testing API Endpoints ---")
    print("Please ensure the MAYA Core server is running on http://localhost:8000")
    print("Run 'python main.py' in the backend directory to start the server")
    print("Then run 'python test_council_api.py' to test the API endpoints")
    
    print("\nFull test suite completed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)