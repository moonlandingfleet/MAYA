import urllib.request
import urllib.error
import json
import os

def test_public_endpoint():
    """Test the public endpoint (should always work)"""
    print("Testing public endpoint...")
    try:
        req = urllib.request.Request('http://localhost:8000/public')
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        print(f"✓ Public endpoint test passed: {data}")
        return True
    except Exception as e:
        print(f"✗ Public endpoint test failed: {e}")
        return False

def test_protected_no_token():
    """Test the protected endpoint without a token (should fail)"""
    print("\nTesting protected endpoint without token...")
    try:
        req = urllib.request.Request('http://localhost:8000/protected')
        response = urllib.request.urlopen(req)
        print(f"✗ Expected this to fail, but got: {response.code}")
        return False
    except urllib.error.HTTPError as e:
        if e.code == 401 or e.code == 403:
            print(f"✓ Protected endpoint correctly rejected request without token: {e.code}")
            return True
        else:
            print(f"✗ Unexpected error code: {e.code}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_protected_with_invalid_token():
    """Test the protected endpoint with an invalid token (should fail)"""
    print("\nTesting protected endpoint with invalid token...")
    try:
        req = urllib.request.Request('http://localhost:8000/protected')
        req.add_header('Authorization', 'Bearer invalid_token_here')
        response = urllib.request.urlopen(req)
        print(f"✗ Expected this to fail, but got: {response.code}")
        return False
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(f"✓ Protected endpoint correctly rejected invalid token: {e.code}")
            return True
        else:
            print(f"✗ Unexpected error code: {e.code}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    print("Running Authentication Tests\n" + "="*40)
    
    # Test 1: Public endpoint (should always work)
    test1_passed = test_public_endpoint()
    
    # Test 2: Protected endpoint without token (should fail)
    test2_passed = test_protected_no_token()
    
    # Test 3: Protected endpoint with invalid token (should fail)
    test3_passed = test_protected_with_invalid_token()
    
    print("\n" + "="*40)
    print("Test Results:")
    print(f"Test 1 (Public endpoint): {'PASS' if test1_passed else 'FAIL'}")
    print(f"Test 2 (No token): {'PASS' if test2_passed else 'FAIL'}")
    print(f"Test 3 (Invalid token): {'PASS' if test3_passed else 'FAIL'}")
    
    all_passed = test1_passed and test2_passed and test3_passed
    print(f"\nOverall Result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    if not all_passed:
        print("\nNote: To test with a valid RS256 token from Supabase, you need to:")
        print("1. Create a test user in your Supabase project")
        print("2. Obtain a valid JWT token using the Supabase REST API")
        print("3. Run a test with that token using curl or a similar tool")
        print("\nExample command:")
        print('curl -H "Authorization: Bearer YOUR_VALID_TOKEN" http://localhost:8000/protected')

if __name__ == "__main__":
    main()