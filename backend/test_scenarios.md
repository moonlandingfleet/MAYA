# Authentication Test Scenarios

## Test Scenario 1: Valid RS256 Token

To test this scenario, you need to:

1. Obtain a JWT token from Supabase:
   - Use the Supabase REST API method to get an access_token for your test user
   - Supabase, by default, issues RS256 tokens for users

2. Call the protected endpoint:
   ```
   GET http://localhost:8000/protected
   Header: Authorization: Bearer <YOUR_RS256_USER_JWT>
   ```

3. Expected Console Output (from auth.py):
   ```
   Attempting RS256 validation...
   (Ideally) Successfully fetched JWKS. (if it's the first time or cache expired)
   RS256 validation successful.
   ```
   
4. Expected API Response: 
   - HTTP 200 OK 
   - Response body: `{"message":"Successfully accessed protected route","user_id":"<user_id_from_token>"}`

## Test Scenario 2: No Token

1. Call the protected endpoint without an Authorization header:
   ```
   GET http://localhost:8000/protected
   ```

2. Expected Response:
   - HTTP 401 Unauthorized
   - Response body: `{"detail":"Not authenticated"}`

## Test Scenario 3: Invalid Token

1. Call the protected endpoint with a bad token:
   ```
   GET http://localhost:8000/protected
   Header: Authorization: Bearer invalid_token_here
   ```

2. Expected Console Output:
   ```
   Attempting RS256 validation...
   RS256 validation failed: ... (some error like "Signature verification failed" or "Invalid token format")
   ```
   
3. Expected API Response:
   - HTTP 401 Unauthorized
   - Response body: `{"detail":"Could not validate credentials - token may be invalid, expired, or lack correct permissions."}`

## How to Obtain a Valid Supabase Token

You can obtain a valid token by:

1. Using the Supabase dashboard to create a test user
2. Using the Supabase JavaScript client library:
   ```javascript
   const { data, error } = await supabase.auth.signInWithPassword({
     email: 'test@example.com',
     password: 'testpassword123'
   });
   const token = data.session.access_token;
   ```

3. Using the Supabase REST API directly:
   ```bash
   curl -X POST 'https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1/token?grant_type=password' \
     -H 'apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtzcnZ0dnFxaWt3amJxenBnYWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc2MzM5ODIsImV4cCI6MjA3MzIwOTk4Mn0.-bI36T8jCKyW8b1n1IFl4yAGZXCd_mqX_r3dma7ytCc' \
     -H 'Content-Type: application/json' \
     -d '{
       "email": "test@example.com",
       "password": "testpassword123"
     }'
   ```