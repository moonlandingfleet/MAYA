# Supabase JWKS Remediation Plan

## Current Status
- **JWKS Endpoint**: Returns `{"keys": []}`
- **Auth Service**: Healthy (GoTrue v2.179.0)
- **Project ID**: `ksrvtvqqikwjbqzpgacs`
- **Issue**: Empty keys array prevents RS256 token validation

## Diagnostic Steps

### Step 1: Run Diagnostic Queries
Execute the queries in [SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql](file:///c%3A/Users/bryan/Desktop/MAYA/maya-core/SUPABASE_SIGNING_KEYS_DIAGNOSTIC.sql) in your Supabase SQL editor.

### Step 2: Check Auth Service Logs
1. Go to Supabase Dashboard → Project → Logs
2. Filter by "auth" service
3. Look for errors related to:
   - Signing key loading
   - JWKS publishing
   - Key rotation

### Step 3: Verify Project Configuration
1. Go to Supabase Dashboard → Project → Authentication → Settings
2. Check for any warnings or errors
3. Verify JWT configuration settings

## Remediation Options (Ordered by Safety)

### Option A: Restart Auth Service (Safest)
**Purpose**: If keys exist but GoTrue failed to load them, a restart may fix the issue.

**How to do it**:
1. Contact Supabase Support with:
   - Project ID: `ksrvtvqqikwjbqzpgacs`
   - Issue: JWKS returns empty keys array
   - Request: Managed restart of Auth service

2. After restart, verify:
   ```bash
   curl https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1/.well-known/jwks.json
   ```

### Option B: Check for Existing Keys (Non-destructive)
If the diagnostic queries show that signing keys exist but have missing/empty public_jwk fields:

**Diagnostic Query**:
```sql
-- Run this if you can access the signing_keys table
SELECT 
    id, 
    kid, 
    alg, 
    public_jwk IS NOT NULL AS has_public_jwk, 
    LENGTH(public_jwk) AS pub_len,
    created_at 
FROM auth.signing_keys 
ORDER BY created_at DESC 
LIMIT 50;
```

**If public_jwk is NULL or empty**:
1. You'll need to reconstruct the public_jwk from stored key material
2. Update the row with the correct public_jwk
3. Restart Auth service

### Option C: Generate New Signing Keys (Requires Explicit Permission)
**Warning**: This is a destructive operation that should only be performed with explicit permission.

**High-level steps**:
1. Generate RSA key pair locally (NOT in the database):
   ```bash
   openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private.pem
   openssl rsa -in private.pem -pubout -out public.pem
   ```

2. Convert public key to JWK format (you can use online tools or scripts)

3. Insert new signing key row:
   ```sql
   INSERT INTO auth.signing_keys (
       id,
       kid,
       alg,
       public_jwk,
       private_key,
       created_at,
       updated_at,
       active
   ) VALUES (
       -- Values to be provided
   );
   ```

4. Restart Auth service

### Option D: Use Supabase Console Key Rotation (If Available)
1. Check if there's a built-in key rotation feature in your Supabase console
2. If available, use it to generate new signing keys
3. Restart Auth service

## Security Considerations

### Private Key Handling
- **Never** share private keys in unencrypted form
- Store private keys securely (environment variables, secrets manager)
- Rotate keys regularly for security

### Database Permissions
- Ensure only the Auth service can read private key values
- Revoke public role access to private columns if necessary

### JWT Token Compatibility
- Ensure JWT tokens are signed with the corresponding private key
- The JWKS must contain the matching `kid` for validation to work

## Validation Steps

After implementing any remediation:

1. **Verify JWKS endpoint**:
   ```bash
   curl https://ksrvtvqqikwjbqzpgacs.supabase.co/auth/v1/.well-known/jwks.json
   ```
   Should return a proper keys array with RSA public keys.

2. **Test RS256 validation**:
   - Obtain a new JWT token from Supabase
   - Test with your MAYA Core API
   - Should succeed without requiring testing mode

3. **Verify existing functionality**:
   - Ensure existing users can still authenticate
   - Check that no existing tokens are invalidated (if keys were rotated)

## Contact Supabase Support

If you're unable to resolve the issue:

**Provide to Support**:
- Project ID: `ksrvtvqqikwjbqzpgacs`
- Issue: JWKS endpoint returns `{"keys": []}`
- Impact: Blocking RS256 validation and production deployment
- Already tried: Diagnostic queries, log checks
- Request: Assistance in repopulating JWKS or managed restart of Auth service

## Expected Outcome

Once resolved:
1. JWKS endpoint returns proper RSA public keys
2. RS256 validation works in production mode
3. No code changes needed in MAYA Core authentication system
4. System ready for production deployment