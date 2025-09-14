# Complete Authentication Test Guide

## Current Test Results

The automated tests for scenarios 2 and 3 have passed:
- Test 2 (No token): PASS - Endpoint correctly returns 403 when no token is provided
- Test 3 (Invalid token): PASS - Endpoint correctly returns 401 when an invalid token is provided

## Test Scenario 1: Valid RS256 Token

To complete the full test suite, you need to test with a valid RS256 token from Supabase.

### Prerequisites

1. Create a test user in your Supabase project:
   - Go to your Supabase dashboard
   - Navigate to Authentication > Users
   - Create a new user with email and password

2. Obtain a valid JWT token using one of these methods:

### Method 1: Using cURL

```bash
curl -X POST 'https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1/token?grant_type=password' \
  -H 'apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzcnZ0dnFxaWt3amJxenBnYWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc2MzM5ODIsImV4cCI6MjA3MzIwOTk4Mn0.-bI36T8jCKyW8b1n1IFl4yAGZXCd_mqX_r3dma7ytCc' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### Method 2: Using Supabase JavaScript Client

```javascript
const { createClient } = supabase;
const supabaseClient = createClient(
  'https://ksrvtvqqikwjbqzpgacs.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzcnZ0dnFxaWt3amJxenBnYWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc2MzM5ODIsImV4cCI6MjA3MzIwOTk4Mn0.-bI36T8jCKyW8b1n1IFl4yAGZXCd_mqX_r3dma7ytCc'
);

const { data, error } = await supabaseClient.auth.signInWithPassword({
  email: 'test@example.com',
  password: 'testpassword123'
});

if (data && data.session) {
  const token = data.session.access_token;
  console.log('Token:', token);
}
```

### Testing with a Valid Token

Once you have a valid token, test the protected endpoint:

```bash
curl -H "Authorization: Bearer YOUR_VALID_TOKEN_HERE" http://localhost:8000/protected
```

### Expected Results

When you make a request with a valid RS256 token, you should see in the server console:

```
Attempting RS256 validation...
(Ideally) Successfully fetched JWKS. (if it's the first time or cache expired)
RS256 validation successful.
```

And the API should return:
- HTTP 200 OK
- Response body: `{"message":"Successfully accessed protected route","user_id":"<user_id_from_token>"}`

### Troubleshooting

If RS256 validation fails, check:

1. Your `.env` file has the correct values:
   - `SUPABASE_JWKS_URI` should point to your Supabase JWKS endpoint
   - `JWT_ALGORITHMS` should include `RS256`
   - `JWT_AUDIENCE` should be set to `authenticated`
   - `JWT_ISSUER` should match your Supabase URL

2. Network connectivity to the Supabase JWKS endpoint

3. Token expiration - make sure you're using a fresh token

## Summary

- Tests 2 and 3 are passing, confirming that the authentication system correctly rejects requests without tokens or with invalid tokens
- To complete the full test suite, you need to verify that a valid RS256 token from Supabase is accepted
- This will confirm that your `.env` configuration is correct for RS256 validation and that `auth.py` is correctly using it